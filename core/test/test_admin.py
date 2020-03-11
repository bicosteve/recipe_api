from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse  # for urls


class AdminSiteTest(TestCase):

    def setUp(self):
        '''runs before every test for checking set ups in our app'''
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email = 'admin@bico.com',
            password = 'password123'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email = 'test@bico.com',
            password = 'password123',
            name = 'Test user full name'
        )

    def test_users_listed(self):
        '''test that users are listed in user page'''
        url = reverse('admin:core_user_changelist') #start with app then url
        response = self.client.get(url)

        self.assertContains(response,self.user.name)
        self.assertContains(response, self.user.email)

    def test_user_change_page(self):
        '''test user edit page works'''
        url = reverse('admin:core_user_change',args=[self.user.id])
        #/admin/core/user/1
        response = self.client.get(url)

        self.assertEqual(response.status_code,200)

    def test_create_user_page(self):
        '''test that crreate user page works'''
        url = reverse('admin:core_user_add')
        response = self.client.get(url)

        self.assertEqual(response.status_code,200)
