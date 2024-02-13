from .models import Customer
from rest_framework import serializers



class CustomerSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of Customer objects."""

    
    class Meta:
        model = Customer
        fields = ["id", "name","code","phone"]

    def create(self, validated_data):
        customer = Customer.objects.create_customer(**validated_data)
        return customer

    