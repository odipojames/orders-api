from rest_framework import generics, status
from rest_framework.response import Response
from .models import Customer
from .serializers import CustomerSerializer
from django.http import Http404
from rest_framework.renderers import JSONRenderer
from utils.decorators import oidc_protected_resource


class CustomerListCreateView(generics.ListCreateAPIView):
    serializer_class = CustomerSerializer
    renderer_classes = (JSONRenderer,)
    
   
    def get_queryset(self):
        """ Listing all customers"""
        
        return Customer.objects.all()
    
    @oidc_protected_resource
    def create(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response = {
            "customer": dict(serializer.data),
            "message": "Customer succesfully added",
        }

        return Response(response, status=status.HTTP_201_CREATED)
    
    
    @oidc_protected_resource
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    

class CustomerDetailView(generics.RetrieveAPIView):
    """
    This class defines the views for retrieving a single customer.
    """

    queryset = Customer.objects.all()  # Queryset for all customers
    serializer_class = CustomerSerializer  # Serializer class for customer objects
    renderer_classes=(JSONRenderer,)
    
    


    def get_object(self):
        """
        Retrieve a single customer by ID.
        """
        customer_id = self.kwargs.get('pk')  #'pk' is the URL parameter for the customer ID
        try:
            customer = Customer.objects.get(pk=customer_id)
            return customer
        except Customer.DoesNotExist:
            raise Http404("Customer does not exist")
        
    @oidc_protected_resource  
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a single customer.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
       

