from unnitest.mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='test@bico.com',password='12345'):
    '''create a sample user'''
    return get_user_model().objects.create_user(email,password)

class ModelTests(TestCase):

    def test_create_user(self):
        '''test creating a new user with an email'''

        email = 'test@bico.com'
        password = 'test123'
        user = get_user_model().objects.create_user(
            email = email,
            password = password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        '''test the email for a new user is normalized'''

        email = 'test@BICO.COM'
        user = get_user_model().objects.create_user(email,'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        '''test creating user with no email raises error'''
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None,'test123')

    def test_create_new_superuser(self):
        '''test creating a new superuser'''
        user = get_user_model().objects.create_superuser(
            'test@bico.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        '''test the tag string representation'''
        tag = models.Tag.objects.create(
            user=sample_user(),
            name = 'vegan'
        )

        self.assertEqual(str(tag),tag.name)

    def  test_ingredient_str(self):
        '''test ingredient string presentation'''
        ingredient = models.Ingredient.objects.create(
            user = sample_user(),
            name = 'Cucumber'
        )

        self.assertEqual(str(ingredient),ingredient.name)

    def test_recipe_str(self):
        '''test recipe string representation'''

        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title = 'Stake and mushroom',
            time_minute=5,
            price=5.00
        )

        self.assertEqual(str(recipe),recipe.title)

    @patch('uuid.uuid4')
    def test_recipe_file_name(self,mock_uuid):
        '''Test that image is saved in correct location'''

        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = modles.recipe_image_file_path(None,'myimage.jpeg')

        exp_path =  f'uploads/recipe/{uuid}.jpeg'
        self.assetEqual(file_path,exp_path)
