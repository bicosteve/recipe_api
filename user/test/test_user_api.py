from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')

def create_user(**params):
    return get_user_model().objects.create_user(**params)



class PublicUserApiTest(TestCase):
    '''Test Users API public'''

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user(self):
        '''Test creating user with valid payload/credential successfull'''
        payload = {
            'email':'bicosteve@gmail.com',
            'password':'naks12345',
            'name':'kibico'
        }

        request = self.client.post(CREATE_USER_URL, payload)

        #test outcome is what we expect
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)

        #test if user is created
        user = get_user_model().objects.get(**request.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password',request.data)


    def test_user_exists(self):
        '''test creating a user already exists'''
        payload={
            'email':'bicosteve@gmail.com',
            'password':'naks12345'
        }
        create_user(**payload)
        request = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)


    def test_password_short(self):
        '''test if the password is more than 5 characters'''
        payload = {'email':'bicosteve@gmail.com','password':'ub'}
        request = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)


    def test_create_token_for_user(self):
        '''test that token is created for user'''
        payload = {
            'email':'bico@bico.com',
            'password':'12345'
        }

        create_user(**payload)
        res = self.client.post(TOKEN_URL,payload)

        self.assertIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        '''test that token is not created with invalid credentials'''
        create_user(email='bico@bico',password='12345')
        payload = {'email':'bico@bico','password':'tut'}

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        '''test that token is not created is user does not exist'''
        payload = {'email':'bico@test.com','password':'test1'}


        res = self.client.post(TOKEN_URL,payload)

        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_token_missing_field(self):
        '''Test that email and password are required'''
        res = self.client.post(TOKEN_URL,{'email':'one','password':''})
        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
