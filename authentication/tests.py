from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import CustomUser as User
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

class UserRegistrationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register_user')
        self.login_url = reverse('login')
        self.username = 'testuser'
        self.password = 'testpassword'

    def test_user_registration(self):
        data = {'username': self.username, 'password': self.password}
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username=self.username).exists())

    def test_user_login(self):
        # Register user
        User.objects.create_user(username=self.username, password=self.password)
        
        # Login with registered user
        data = {'username': self.username, 'password': self.password}
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)


