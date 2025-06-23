"""Websockets"""
import logging
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Client, Message, ClientLastPoll
from .serializers import MessageSerializer

logger = logging.getLogger(__name__)

class MessageConsumer(AsyncJsonWebsocketConsumer):
    """WebSocket consumer for handling global real-time messaging."""
    
    async def connect(self):
        """Handle WebSocket connection."""
        self.client_id = self.scope['url_route']['kwargs']['client_id']
        
        try:
            self.client = await database_sync_to_async(Client.objects.get)(client_id=self.client_id)
        except Client.DoesNotExist:
            self.client = await database_sync_to_async(Client.objects.create)(client_id=self.client_id)
            await database_sync_to_async(ClientLastPoll.objects.create)(client=self.client)
        
        # Join a global group for all clients
        self.group_name = "global_chat"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        
        # Send initial message to confirm connection
        await self.send_json({
            'type': 'connection_established',
            'message': f'Connected as client {self.client_id}'
        })
        
        # Start sending new messages
        await self.send_new_messages()

    async def disconnect(self, close_code):
        """Handle WebSocket disconnection."""
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        logger.info(f"Client {self.client_id} disconnected with code {close_code}")

    async def receive_json(self, content):
        """Handle incoming WebSocket messages."""
        message_type = content.get('type')
        if message_type == 'message':
            message_content = content.get('content')
            if not message_content:
                await self.send_json({
                    'type': 'error',
                    'message': 'Content is required'
                })
                return
                
            # Create new message
            message = await database_sync_to_async(Message.objects.create)(
                client=self.client,
                content=message_content
            )
            
            # Serialize message
            serializer = MessageSerializer(message)
            serialized_data = await database_sync_to_async(lambda: serializer.data)()
            
            # Broadcast to global group
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'new_message',
                    'message': serialized_data
                }
            )

    async def new_message(self, event):
        """Handle new message events."""
        await self.send_json({
            'type': 'message',
            'data': event['message']
        })

    async def send_new_messages(self):
        """Send new messages to the client since last polled."""
        last_polled_obj = await database_sync_to_async(ClientLastPoll.objects.get)(client=self.client)
        last_polled = last_polled_obj.last_polled
        
        new_messages = await database_sync_to_async(
            lambda: Message.objects.filter(timestamp__gt=last_polled).select_related('client')
        )()
        
        if await database_sync_to_async(new_messages.exists)():
            serializer = MessageSerializer(new_messages, many=True)
            serialized_data = await database_sync_to_async(lambda: serializer.data)()
            
            for message in serialized_data:
                await self.send_json({
                    'type': 'message',
                    'data': message
                })
                
            await database_sync_to_async(last_polled_obj.update_last_polled)()
