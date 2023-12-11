from typing import Optional

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from recipe.models import Recipe
from recipe.serializers import RecipeSerializer


class TestRecipeSerializer(TestCase):
    def setUp(self):
        # Create a valid chef
        self.chef = User.objects.create_user(
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
            'chef': self.chef,
        }

        # Create a recipe instance
        self.recipe_instance = Recipe.objects.create(**self.validated_data)

    def test_serializer_valid_data_create_update(self):
        # Create a serializer with valid data
        serializer = RecipeSerializer(data=self.validated_data, chef=self.chef)
        # Check if serializer is valid
        self.assertTrue(serializer.is_valid())
        validated_data = serializer.validated_data
        # Check if validated data is correct
        for key, value in self.validated_data.items():
            self.assertEqual(value, validated_data[key])
        # Check save method
        recipe = serializer.save()
        self.assertIsInstance(recipe, Recipe)
        # Update validated data
        validated_data_update = {
            'name': self.validated_data['name'] + ' updated',
            'description': self.validated_data['description'] + ' updated',
            'ingredients': self.validated_data['ingredients'] + ' updated',
            'instructions': self.validated_data['instructions'] + ' updated',
            'prep_time': self.validated_data['prep_time'] + timezone.timedelta(minutes=5),
            'cook_time': self.validated_data['cook_time'] + timezone.timedelta(minutes=5),
            'servings': self.validated_data['servings'] + 5,
        }
        # Create a serializer with valid data
        serializer = RecipeSerializer(instance=recipe, data=validated_data_update, chef=self.chef)
        # Check if serializer is valid
        self.assertTrue(serializer.is_valid())
        validated_data = serializer.validated_data
        # Check if validated data is correct
        for key, value in validated_data_update.items():
            self.assertEqual(value, validated_data[key])
        # Check save method
        recipe = serializer.save()
        self.assertIsInstance(recipe, Recipe)

    def invalid_value_field_test(
            self, field_name: str, possible_errors: list, instance: Optional[Recipe] = None
    ) -> None:
        """
        Test a given field with a set of possible errors
        :param field_name: Name of the field to be tested
        :param possible_errors: List with possible errors
        :param instance: Instance of Recipe
        """
        # Try creating a recipe with an invalid value for a given field
        validated_data = self.validated_data.copy()
        validated_data.pop(field_name, None)

        for message_error, type_error, value in possible_errors:
            with self.assertRaises(type_error) as context:
                if isinstance(value, list):
                    for v in value:
                        serializer = RecipeSerializer(instance=instance, data=validated_data, chef=self.chef)
                        serializer.is_valid(raise_exception=True)
                        serializer.save(**{field_name: v})
                else:
                    serializer = RecipeSerializer(instance=instance, data=validated_data, chef=self.chef)
                    serializer.is_valid(raise_exception=True)
                    serializer.save(**{field_name: value})

            # Check if validation was triggered correctly
            self.assertIn(message_error, str(context.exception))

    def test_serializer_invalid_name_field(self):
        # Test name field with invalid values
        possible_errors = [
            ('This field is required.', ValidationError, [None, '', ' ', 'a' * 256]),
        ]
        # Test name field with invalid values for create
        self.invalid_value_field_test(field_name='name', possible_errors=possible_errors)
        # Test name field with invalid values for update
        self.invalid_value_field_test(field_name='name', possible_errors=possible_errors, instance=self.recipe_instance)

    def test_serializer_valid_description_field(self):
        # Test description field with valid values
        possible_values = [
            '',
            'a' * 1001,
            None,
        ]
        for value in possible_values:
            serializer = RecipeSerializer(instance=self.recipe_instance, data=self.validated_data, chef=self.chef)
            self.assertTrue(serializer.is_valid(raise_exception=True))
            recipe = serializer.save(description=value)
            self.assertIsInstance(recipe, Recipe)
            self.assertEqual(recipe.description, value)

    def test_serializer_invalid_ingredients_field(self):
        # Test ingredients field with invalid values
        possible_errors = [
            ('This field is required.', ValidationError, [None, '', ' ']),
        ]
        # Test ingredients field with invalid values for create
        self.invalid_value_field_test(field_name='ingredients', possible_errors=possible_errors)
        # Test ingredients field with invalid values for update
        self.invalid_value_field_test(
            field_name='ingredients', possible_errors=possible_errors, instance=self.recipe_instance
        )

    def test_serializer_invalid_instructions_field(self):
        # Test instructions field with invalid values
        possible_errors = [
            ('This field is required.', ValidationError, [None, '', ' ']),
        ]
        # Test instructions field with invalid values for create
        self.invalid_value_field_test(field_name='instructions', possible_errors=possible_errors)
        # Test instructions field with invalid values for update
        self.invalid_value_field_test(
            field_name='instructions', possible_errors=possible_errors, instance=self.recipe_instance
        )

    def test_serializer_invalid_prep_time_field(self):
        # Test prep_time field with invalid values
        possible_errors = [
            ('This field is required.', ValidationError, [timezone.timedelta(minutes=-1), None, '', ' ']),
        ]
        # Test prep_time field with invalid values for create
        self.invalid_value_field_test(field_name='prep_time', possible_errors=possible_errors)
        # Test prep_time field with invalid values for update
        self.invalid_value_field_test(
            field_name='prep_time', possible_errors=possible_errors, instance=self.recipe_instance
        )

    def test_serializer_invalid_cook_time_field(self):
        # Test cook_time field with invalid values
        possible_errors = [
            ('This field is required.', ValidationError, [timezone.timedelta(minutes=-1), None, '', ' ']),
        ]
        # Test cook_time field with invalid values for create
        self.invalid_value_field_test(field_name='cook_time', possible_errors=possible_errors)
        # Test cook_time field with invalid values for update
        self.invalid_value_field_test(
            field_name='cook_time', possible_errors=possible_errors, instance=self.recipe_instance
        )

    def test_serializer_invalid_servings_field(self):
        # Test servings field with invalid values
        possible_errors = [
            ("Field 'servings' expected a number but got ''.", ValueError, ''),
        ]
        # Test servings field with invalid values for create
        self.invalid_value_field_test(field_name='servings', possible_errors=possible_errors)
        # Test servings field with invalid values for update
        self.invalid_value_field_test(
            field_name='servings', possible_errors=possible_errors, instance=self.recipe_instance
        )

    def test_serializer_invalid_chef_field(self):
        # Test chef field with valid values
        validated_data = self.validated_data.copy()
        validated_data.pop('chef', None)
        serializer = RecipeSerializer(instance=self.recipe_instance, data=validated_data)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
        # Check if validation was triggered correctly
        self.assertIn('Only chefs can register recipes', str(context.exception))
        self.assertFalse(serializer.is_valid(raise_exception=False))
