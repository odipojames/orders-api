from .models import Order
from rest_framework import serializers
from customers.serializers import CustomerSerializer  
from customers.models import Customer

class OrderSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of Order objects."""

    # Define the customer field to accept only the customer ID during creation
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())

    class Meta:
        model = Order
        fields = ["id", "item", "amount", "customer", "created_at"]
        extra_kwargs = {"id": {"read_only": True}, "created_id": {"read_only": True}}

    def create(self, validated_data):
        order = Order.objects.create_order(**validated_data)
        return order

    # Override the to_representation method to include the full customer object in the response
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Retrieve the full customer object
        customer = instance.customer
        # Serialize the customer object using CustomerSerializer
        customer_data = CustomerSerializer(customer).data
        # Replace the customer ID with the serialized customer object
        representation['customer'] = customer_data
        return representation
