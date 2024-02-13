from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse
from customers.models import Customer
from customers.serializers import CustomerSerializer
from rest_framework.authtoken.models import Token



class CustomerListCreateViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        
        # Create a token for the test user
        self.token = Token.objects.create(user=self.user)
            
    def test_list_customers(self):
        # Create some customers for testing
        customer1 = Customer.objects.create_customer(name='Customer 1', phone='+1234567890')
        customer2 = Customer.objects.create_customer(name='Customer 2', phone='+9876543210')

        url = reverse('create-list-customers')
        
        # Include the token in the Authorization header
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token.key)
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        expected_data = CustomerSerializer(instance=[customer1, customer2], many=True).data
        self.assertEqual(response.data, expected_data)

    

class CustomerAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.customer_data = {'name': 'Test Customer',  'phone': '+1234567890'}
        self.customer = Customer.objects.create_customer(**self.customer_data)
        
        # Create a token for the test user
        self.token = Token.objects.create(user=self.user)

    def test_retrieve_customer(self):
        url = reverse('customer-details', kwargs={'pk': self.customer.pk})
        
        # Include the token in the Authorization header
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token.key)
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        expected_data = CustomerSerializer(instance=self.customer).data
        self.assertEqual(response.data, expected_data)
