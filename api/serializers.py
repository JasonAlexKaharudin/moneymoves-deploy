from rest_framework import serializers
from .models import WebhookOrder

class webhookSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebhookOrder
        fields = ['merchant_name','discount_code', 'order_id', 'total_price']