from rest_framework.response import Response
from rest_framework import status,generics
from rest_framework.renderers import JSONRenderer
from  .serializers import OrderSerializer
from .models import Order
from django.http import Http404
from utils.decorators import oidc_protected_resource
from utils.helpers import send_sms
from customers.models import Customer





class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    renderer_classes = (JSONRenderer,)
    
  
    def get_queryset(self):
        """Listing all orders"""
        
        return Order.objects.all()
    
    @oidc_protected_resource
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    
    @oidc_protected_resource
    def create(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        #get phone of the passed customer
        customer_id =  serializer.validated_data.get('customer').pk
        customer = Customer.objects.get(id=customer_id)
        serializer.save()
        #send sms to customer
        send_sms(
                    message="Odipo Has dispatched your order!",
                    recipients=[customer.phone,],
                )

        response = {
            "order": dict(serializer.data),
            "message": "Order succesfully created",
        }

        return Response(response, status=status.HTTP_201_CREATED)



class OrderDetailView(generics.RetrieveAPIView):
    """
    This class defines the views for retrieving a single order.
    """

    queryset = Order.objects.all()  # Queryset for all orders
    serializer_class = OrderSerializer  # Serializer class for order objects
    renderer_classes = (JSONRenderer,)
    
    
    

    def get_object(self):
        """
        Retrieve a single order by ID.
        """
        order_id = self.kwargs.get('pk')  #'pk' is the URL parameter for the order ID
        try:
            order = Order.objects.get(pk=order_id)
            return order
        except Order.DoesNotExist:
            raise Http404("Order does not exist")
        
    @oidc_protected_resource    
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a single order.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
       