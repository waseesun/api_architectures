from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['order_id', 'status', 'amount', 'payment_id', 'product_id', 'quantity', 'updated_at']