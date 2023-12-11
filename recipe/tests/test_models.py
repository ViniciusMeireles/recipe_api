from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from django.utils import timezone

from recipe.models import Recipe


class TestRecipeModel(TestCase):

    def setUp(self):
        # Create a valid chef
        chef = User.objects.create_user(
            username='testchef' + str(timezone.now().timestamp()) + str(range(1000)),
            password='testpassword',
        )
        name = 'Bolinho de bacalhau'
        description = (
            'Bolinho de bacalhau é figurinha marcada na ceia de Natal e também como entrada ou petisco em '
            'bares e restaurantes. A tradição do aperitivo vem da gastronomia portuguesa e ele é encontrado '
            'em diversas partes do Brasil.\r\n'
            'https://receitas.globo.com/receitas-da-tv/mais-voce/bolinho-de-bacalhau-sem-erro-52bd64c64d38851fb300003f'
            '.ghtml'
        )
        ingredients = ('1 colher de sopa de azeite\r\nMeia colher de sopa de alho\r\n2 colheres de sopa de cebola '
                       'picadinha\r\n2 batatas médias cozidas, descascadas e amassadas\r\n1 ovo batido\r\n200 gramas, '
                       'ou uma xícara de chá de bacalhau cozido e desfiado\r\nUm quarto de uma de xícara de chá, ou 30 '
                       'gramas de farinha de rosca\r\n1 colher de sopa de azeite\r\nSalsinha picadinha a gosto\r\n'
                       'Pimenta-do-reino moída a gosto\r\nSal a gosto')
        instructions = ('1\r\nNuma panela com 1 colher de sopa de azeite, refogue meia colher de sopa de alho, 2 '
                        'colheres de sopa de cebola picadinha até dourar.\r\n2\r\nTransfira o refogado para numa '
                        'tigela.\r\n3\r\nAdicione 2 batatas médias cozidas e amassadas, 1 ovo batido, 200 gramas de '
                        'bacalhau cozido e desfiado, um quarto de uma de xícara de chá de farinha de rosca, 1 colher '
                        'de sopa de azeite, salsa picadinha, pimenta-do-reino moída, sal a gosto.\r\n4\r\nMisture bem '
                        'até formar uma massa homogênea. Pegue pequenas porções de massa, faça bolinhas e frite em '
                        'óleo quente até dourar.\r\n5\r\nRetire, escorra em papel absorvente e sirva em seguida.')
        prep_time = timezone.timedelta(minutes=45)
        cook_time = timezone.timedelta(minutes=0)
        servings = 20

        # Save the validated data
        self.validated_data = {
            'name': name,
            'description': description,
            'ingredients': ingredients,
            'instructions': instructions,
            'prep_time': prep_time,
            'cook_time': cook_time,
            'servings': servings,
            'chef': chef,
        }

    def invalid_value_field_test(self, field_name: str, possible_errors: list) -> None:
        """
        Test a given field with a set of possible errors
        :param field_name: Name of the field to be tested
        :param possible_errors: List with possible errors
        """
        # Try creating a recipe with an invalid value for a given field
        validated_data = self.validated_data.copy()
        validated_data.pop(field_name, None)

        for message_error, type_error, value in possible_errors:
            with self.assertRaises(type_error) as context:
                if isinstance(value, list):
                    for v in value:
                        recipe = Recipe.objects.create(
                            **validated_data,
                            **{field_name: v},  # Invalid value
                        )
                        recipe.full_clean()
                        recipe.save()
                else:
                    recipe = Recipe.objects.create(
                        **validated_data,
                        **{field_name: value},  # Invalid value
                    )
                    recipe.full_clean()
                    recipe.save()

            # Check if validation was triggered correctly
            self.assertIn(message_error, str(context.exception))

    def test_create_recipe(self):
        # Create a valid recipe
        recipe = Recipe.objects.create(
            **self.validated_data,
        )

        # Check if the recipe was saved correctly
        for field_name in self.validated_data.keys():
            self.assertEqual(getattr(recipe, field_name), self.validated_data.get(field_name))

    def test_invalid_name(self):
        # Try creating a recipe with an invalid name
        possible_errors = [
            ('This field cannot be blank.', ValidationError, ''),
            ('Ensure this value has at most 255 characters (it has 256).', ValidationError, 'a' * 256),
            ('NOT NULL constraint failed: recipe_recipe.name', IntegrityError, None),
        ]
        self.invalid_value_field_test('name', possible_errors)

    def test_valid_description(self):
        # Try creating a recipe with a valid description
        validated_data = self.validated_data.copy()
        validated_data.pop('description', None)
        for value in ['', 'a' * 1001, None]:
            recipe = Recipe.objects.create(
                **validated_data,
                description=value,
            )
            recipe.full_clean()
            recipe.save()
            self.assertEqual(recipe.description, value)

    def test_invalid_ingredients(self):
        # Try creating a recipe with invalid ingredients
        possible_errors = [
            ('This field cannot be blank.', ValidationError, ''),
            ('NOT NULL constraint failed: recipe_recipe.ingredients', IntegrityError, None),
        ]
        self.invalid_value_field_test('ingredients', possible_errors)

    def test_invalid_instructions(self):
        # Try creating a recipe with invalid instructions
        possible_errors = [
            ('This field cannot be blank.', ValidationError, ''),
            ('NOT NULL constraint failed: recipe_recipe.instructions', IntegrityError, None),
        ]
        self.invalid_value_field_test('instructions', possible_errors)

    def test_invalid_prep_time(self):
        # Try creating a recipe with an invalid preparation time
        possible_errors = [
            ('Preparation time must be equal to or greater than 1 minute.', ValidationError,
             timezone.timedelta(minutes=0)),
            ('NOT NULL constraint failed: recipe_recipe.prep_time', IntegrityError, None),
            ("'str' object has no attribute 'days'", AttributeError, ['abc', '']),
        ]
        self.invalid_value_field_test('prep_time', possible_errors)

    def test_invalid_cook_time(self):
        # Try creating a recipe with an invalid cooking time
        possible_errors = [
            ('Cooking time must be equal to or greater than 0 minutes.', ValidationError,
             timezone.timedelta(minutes=-1)),
            ('NOT NULL constraint failed: recipe_recipe.cook_time', IntegrityError, None),
            ("'str' object has no attribute 'days'", AttributeError, ['abc', '']),
        ]
        self.invalid_value_field_test('cook_time', possible_errors)

    def test_invalid_servings(self):
        # Try creating a recipe with an invalid number of servings
        possible_errors = [
            ('Servings must be equal to or greater than 1.', ValidationError, 0),
            ('NOT NULL constraint failed: recipe_recipe.servings', IntegrityError, None),
            ("Field 'servings' expected a number but got 'abc'.", ValueError, 'abc'),
        ]
        self.invalid_value_field_test('servings', possible_errors)

    def test_invalid_chef(self):
        # Try creating a recipe with an invalid chef
        possible_errors = [
            ("NOT NULL constraint failed: recipe_recipe.chef_id",
             IntegrityError, None),
            ('Cannot assign "-1": "Recipe.chef" must be a "User" instance.', ValueError, -1),
        ]
        self.invalid_value_field_test('chef', possible_errors)
