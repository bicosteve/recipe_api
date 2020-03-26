from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase


from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe
from recipe_app.serializers import RecipeSerializer


RECIPES_URL = reverse('recipe_app:recipe-list')


def sample_recipe(user, **params):
    '''create and returns sample recipe'''

    defaults = {
        'title':'Sample Recipe',
        'time':10,
        'price':5.00
    }

    defaults.update(params)

    return Recipe.objects.create(user=user, **defaults)


class PublicRecipeApiTest(TestCase):
    '''Test unauthenticated recipe Api access'''

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        '''test that authentication is required'''

        res = self.client.get(RECIPES_URL)

        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTest(TestCase):
    '''test unauthenticated recipe apit access'''

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'bico@test.com',
            'testpass'
        )

        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        '''testing retrieving a list of recipes'''

        sample_recipe(user=self.user)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes,many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipe_limited_to_user(self):
        '''test retrieving recipe for user'''

        user2 = get_user_model().objects.create_user(
            'other@bico.com',
            'passtest'
        )
        sample_recipe(user=user2)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes,many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data),1)
        self.assertEqual(res.data, serializer.data)
