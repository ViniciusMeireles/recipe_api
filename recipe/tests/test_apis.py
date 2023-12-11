from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from recipe.models import Recipe


class TestRecipeAPI(APITestCase):
    def setUp(self):
        self.url = '/recipes/'
        self.chef = User.objects.create_user(
            username='testchef' + str(timezone.now().timestamp()) + str(range(1000)),
            password='testpassword',
        )
        token = Token.objects.create(user=self.chef)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        self.client.force_authenticate(user=self.chef)

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
            'chef': self.chef.id,
        }

    def test_create_recipe(self):
        # Try creating a recipe with valid data
        response = self.client.post(self.url, self.validated_data, format='json')
        self.assertEqual(response.status_code, 201)
        data = response.data
        for key, value in self.validated_data.items():
            if key == 'chef':
                self.assertEqual(data[key], self.chef.username)
            elif key == 'prep_time' or key == 'cook_time':
                self.assertEqual(data[key], '0' + str(value))
            else:
                self.assertEqual(data[key], value)

    def test_create_recipe_without_authentication(self):
        # Try creating a recipe without authentication
        self.client.force_authenticate(user=None)
        response = self.client.post(self.url, self.validated_data, format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_create_recipe_with_invalid_data(self):
        # Try creating a recipe with invalid data
        validated_data = self.validated_data.copy()
        validated_data.pop('name', None)
        response = self.client.post(self.url, validated_data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['name'][0], 'This field is required.')

    def test_update_recipe(self):
        # Try updating a recipe with valid data
        validated_data = self.validated_data.copy()
        validated_data['chef'] = self.chef
        recipe = Recipe.objects.create(**validated_data)
        response = self.client.put(self.url + str(recipe.id) + '/', self.validated_data, format='json')
        self.assertEqual(response.status_code, 200)
        data = response.data
        for key, value in self.validated_data.items():
            if key == 'chef':
                self.assertEqual(data[key], self.chef.username)
            elif key == 'prep_time' or key == 'cook_time':
                self.assertEqual(data[key], '0' + str(value))
            else:
                self.assertEqual(data[key], value)

    def test_update_recipe_without_authentication(self):
        # Try updating a recipe without authentication
        validated_data = self.validated_data.copy()
        validated_data['chef'] = self.chef
        recipe = Recipe.objects.create(**validated_data)
        self.client.force_authenticate(user=None)
        response = self.client.put(self.url + str(recipe.id) + '/', self.validated_data, format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_update_recipe_with_invalid_data(self):
        # Try updating a recipe with invalid data
        validated_data = self.validated_data.copy()
        validated_data['chef'] = self.chef
        recipe = Recipe.objects.create(**validated_data)
        self.validated_data.pop('name', None)
        response = self.client.put(self.url + str(recipe.id) + '/', self.validated_data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['name'][0], 'This field is required.')

    def test_list_recipes(self):
        # Try listing recipes
        validated_data = self.validated_data.copy()
        validated_data['chef'] = self.chef
        Recipe.objects.create(**validated_data)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        data = response.data[0]
        for key, value in self.validated_data.items():
            if key == 'chef':
                self.assertEqual(data[key], self.chef.username)
            elif key == 'prep_time' or key == 'cook_time':
                self.assertEqual(data[key], '0' + str(value))
            else:
                self.assertEqual(data[key], value)

    def test_list_recipes_without_authentication(self):
        # Try listing recipes without authentication
        validated_data = self.validated_data.copy()
        validated_data['chef'] = self.chef
        Recipe.objects.create(**validated_data)
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        data = response.data[0]
        for key, value in self.validated_data.items():
            if key == 'chef':
                self.assertEqual(data[key], self.chef.username)
            elif key == 'prep_time' or key == 'cook_time':
                self.assertEqual(data[key], '0' + str(value))
            else:
                self.assertEqual(data[key], value)

    def test_retrieve_recipe(self):
        # Try retrieving a recipe
        validated_data = self.validated_data.copy()
        validated_data['chef'] = self.chef
        recipe = Recipe.objects.create(**validated_data)
        response = self.client.get(self.url + str(recipe.id) + '/')
        self.assertEqual(response.status_code, 200)
        data = response.data
        for key, value in self.validated_data.items():
            if key == 'chef':
                self.assertEqual(data[key], self.chef.username)
            elif key == 'prep_time' or key == 'cook_time':
                self.assertEqual(data[key], '0' + str(value))
            else:
                self.assertEqual(data[key], value)

    def test_retrieve_recipe_without_authentication(self):
        # Try retrieving a recipe without authentication
        validated_data = self.validated_data.copy()
        validated_data['chef'] = self.chef
        recipe = Recipe.objects.create(**validated_data)
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url + str(recipe.id) + '/')
        self.assertEqual(response.status_code, 200)
        data = response.data
        for key, value in self.validated_data.items():
            if key == 'chef':
                self.assertEqual(data[key], self.chef.username)
            elif key == 'prep_time' or key == 'cook_time':
                self.assertEqual(data[key], '0' + str(value))
            else:
                self.assertEqual(data[key], value)

    def test_delete_recipe(self):
        # Try deleting a recipe
        validated_data = self.validated_data.copy()
        validated_data['chef'] = self.chef
        recipe = Recipe.objects.create(**validated_data)
        response = self.client.delete(self.url + str(recipe.id) + '/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data, None)

    def test_delete_recipe_without_authentication(self):
        # Try deleting a recipe without authentication
        validated_data = self.validated_data.copy()
        validated_data['chef'] = self.chef
        recipe = Recipe.objects.create(**validated_data)
        self.client.force_authenticate(user=None)
        response = self.client.delete(self.url + str(recipe.id) + '/')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_delete_recipe_with_invalid_id(self):
        # Try deleting a recipe with an invalid id
        validated_data = self.validated_data.copy()
        validated_data['chef'] = self.chef
        recipe = Recipe.objects.create(**validated_data)
        response = self.client.delete(self.url + str(recipe.id + 1) + '/')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['detail'], 'Not found.')

    def test_filter_recipes_by_name(self):
        # Try filtering recipes by name
        validated_data = self.validated_data.copy()
        validated_data['chef'] = self.chef
        Recipe.objects.create(**validated_data)
        response = self.client.get(self.url + '?name=' + validated_data['name'])
        self.assertEqual(response.status_code, 200)
        data = response.data[0]
        for key, value in self.validated_data.items():
            if key == 'chef':
                self.assertEqual(data[key], self.chef.username)
            elif key == 'prep_time' or key == 'cook_time':
                self.assertEqual(data[key], '0' + str(value))
            else:
                self.assertEqual(data[key], value)

    def test_filter_recipes_by_chef(self):
        # Try filtering recipes by chef
        validated_data = self.validated_data.copy()
        validated_data['chef'] = self.chef
        Recipe.objects.create(**validated_data)
        response = self.client.get(self.url + '?chef=' + str(self.chef.username))
        self.assertEqual(response.status_code, 200)
        data = response.data[0]
        for key, value in self.validated_data.items():
            if key == 'chef':
                self.assertEqual(data[key], self.chef.username)
            elif key == 'prep_time' or key == 'cook_time':
                self.assertEqual(data[key], '0' + str(value))
            else:
                self.assertEqual(data[key], value)
