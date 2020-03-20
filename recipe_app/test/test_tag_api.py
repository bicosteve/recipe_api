from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag

from recipe_app.serializers import TagSerializer

TAGS_URL = reverse('recipe_app:tag-list')

def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicTagsApiTest(TestCase):
    '''Test the publicly avaiable tags API'''

    def setUp(self):
        self.client = APIClient

    def test_login_required(self):
        '''test that login is required for retrieving tags'''
        payload = {
            'email':'kimani@kimani.com',
            'password':'pass123'
        }
        
        create_user(**payload)
        res = self.client.get(TAGS_URL,payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTest(TestCase):
    '''Test the authorized user tag API'''

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'bico@bico.com',
            'password12'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        '''Test retrevient tags'''
        Tag.objects.create(user=self.user,name='Vegan')
        Tag.objects.create(user=self.user,name='Dessert')

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer =TagSerializer(tags,many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data,serializer.data)

    def test_tags_limited_to_user(self):
        '''test that tags returned is for authenticated user'''
        user_two = get_user_model().objects.create_user(
            'karo@karo.com',
            'testpass'
        )
        Tag.objects.create(user=user_two,name='Juice')
        tag = Tag.objects.create(user=self.user, name = 'Staple')

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(len(res.data),1)
        self.assertEqual(res.data[0]['name'],tag.name)
