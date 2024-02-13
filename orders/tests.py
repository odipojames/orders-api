from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse
from orders.models import Order
from orders.serializers import OrderSerializer
from customers.models import Customer
from rest_framework.authtoken.models import Token


class OrderAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.customer = Customer.objects.create_customer(name='Test Customer', phone='+1234567890')
        
    def test_list_orders(self):
        order1 = Order.objects.create_order(customer=self.customer, amount=100,item="tv")
        order2 = Order.objects.create_order(customer=self.customer, amount=200,item="phone")

        url = reverse('create-list-order')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token.key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        expected_data = OrderSerializer(instance=[order1, order2], many=True).data
        self.assertEqual(response.data, expected_data)

    
    def test_retrieve_order(self):
        order = Order.objects.create_order(customer=self.customer, amount=300,item='tv')
        url = reverse('order-details', kwargs={'pk': order.pk})
        
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token.key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        expected_data = OrderSerializer(instance=order).data
        self.assertEqual(response.data, expected_data)
