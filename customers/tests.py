from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Customer
from .serializers import CustomerSerializer


class CustomerDetailViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer = Customer.objects.create(name='Test Customer', phone='+254707371208')
        self.url = f'/api/v1/customers/{self.customer.pk}/'  
        
    def test_retrieve_customer(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.customer.name)
        self.assertEqual(response.data['phone'], self.customer.phone)

    def test_retrieve_nonexistent_customer(self):
        nonexistent_id = self.customer.pk + 1  # Assuming ID doesn't exist
        url = f'/api/v1/customers/{nonexistent_id}/' 
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
