from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase


from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient

from recipe_app.serializers import IngredientSerializer


INGREDIENTS_URL = reverse('recipe_app:ingredient-list')


class PublicIngredientApiTest(TestCase):
    '''test for publicly available api'''

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        '''Test that login is required to access this end point'''

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientApiTest(TestCase):
    '''test the private api '''

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@bico.com',
            'testpass'
        )

        self.client.force_authenticate(self.user)

        def test_retrieve_ingredient_list(self):
            '''test retreiving a list of ingredients'''

            Ingredient.objects.create(user=self.user, name='Sukuma')
            Ingredient.objects.create(user=self.user,name='Chipo')

            res =  self.client.get(INGREDIENTS_URL)

            ingredients = Ingredient.object.all().order_by('-name')
            serializer = IngredientSerializer(ingredients,many=True)

            self.assertEqual(res.status_code, status.HTTP_200_OK)
            self.assertEqual(res.data, serializer.data)

        def test_ingredients_limited_to_user(self):
            '''test ingredient for only authenticated user is returned'''
            user2 = get_user_model().objects.create_user(
                'other@bico.com',
                'passtest123'
            )

            Ingredient.objects.create(user=user2,name='Fish')
            ingredient = Ingredient.objects.create(user=self.user,name='Kales')

            res = self.client.get(INGREDIENTS_URL)

            self.assertEqual(res.status_code, status.HTTP_200_OK)
            self.assertEqual(len(res.data),1)
            self.assertEqual(res.data[0],ingredient.name)

        def test_create_ingredient_successful(self):
            '''test create a new ingredient'''

            payload = {'name':'Cabbage'}
            self.client.post(INGREDIENTS_URL,payload)

            exists = Ingredient.objects.filter(
                user=self.user,
                name=payload['name'],
            ).exists()
            self.assertTrue(exists)

        def test_ingredient_invalid(self):
            '''test creating creating invalid ingredient fails'''
            payload = {'name':''}
            res = self.client.post(INGREDIENTS_URL,payload)

            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
