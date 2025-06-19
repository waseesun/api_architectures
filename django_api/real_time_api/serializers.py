from rest_framework import serializers
from .models import Client, Message, ClientLastPoll

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['client_id', 'created_at']

class MessageSerializer(serializers.ModelSerializer):
    client_id = serializers.UUIDField(source='client.client_id', allow_null=True)

    class Meta:
        model = Message
        fields = ['id', 'client_id', 'content', 'timestamp']
        read_only_fields = ['id', 'timestamp']

class ClientLastPollSerializer(serializers.ModelSerializer):
    client_id = serializers.UUIDField(source='client.client_id')

    class Meta:
        model = ClientLastPoll
        fields = ['client_id', 'last_polled']
        read_only_fields = ['last_polled']