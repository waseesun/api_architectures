from rest_framework import serializers
from .models import WebhookEvent

class WebhookEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebhookEvent
        fields = ['id', 'event_type', 'payload', 'received_at', 'processed', 'product']
        read_only_fields = ['id', 'received_at', 'processed']