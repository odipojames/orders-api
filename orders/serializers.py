from .models import Order
from rest_framework import serializers



class OrderSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of Order objects."""

    
    class Meta:
        model = Order
        fields = ["id", "item","amount","customer","created_at"]
        extra_kwargs = {"id": {"read_only": True}, "created_id": {"read_only": True}}


    def create(self, validated_data):
        order = Order.objects.create_order(**validated_data)
        return order