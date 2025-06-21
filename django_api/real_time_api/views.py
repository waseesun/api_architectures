"""
Views for short and long polling, SSE (Server-Sent Events) and WebSockets.
"""
import json
import time
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import StreamingHttpResponse
from django.utils import timezone
from django_api.renderers import ViewRenderer
from .models import Client, Message, ClientLastPoll
from .serializers import MessageSerializer


class SendMessageView(APIView):
    """Send a message to a client."""
    renderer_classes = [ViewRenderer]
    
    def post(self, request):
        client_id = request.data.get('client_id')
        content = request.data.get('content')
        
        if not client_id or not content:
            return Response(
                {'error': 'client_id and content are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            client = Client.objects.get(client_id=client_id)
        except Client.DoesNotExist:
            client = Client.objects.create(client_id=client_id)
            ClientLastPoll.objects.create(client=client)
            
        message = Message.objects.create(client=client, content=content)
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PollMessagesView(APIView):
    """Short and long polling."""
    renderer_classes = [ViewRenderer]
    
    def get(self, request):
        client_id = request.query_params.get('client_id')
        # Defaults to short polling
        polling_type = request.query_params.get('polling_type', 'short')
        
        if not client_id:
            return Response(
                {'error': 'client_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            client = Client.objects.get(client_id=client_id)
        except Client.DoesNotExist:
            client = Client.objects.create(client_id=client_id)
            ClientLastPoll.objects.create(client=client)
            
        last_polled = ClientLastPoll.objects.get(client=client).last_polled
        
        if polling_type == "long":
            timeout = 30  # seconds
            start_time = time.time()
            
            while time.time() - start_time < timeout:
                new_messages = Message.objects.filter(timestamp__gt=last_polled
                ).select_related('client')
                
                if new_messages.exists():
                    ClientLastPoll.objects.get(client=client).update_last_polled()
                    serializer = MessageSerializer(new_messages, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                
                time.sleep(1)  # Wait for 1 second before checking again
                
            return Response([], status=status.HTTP_200_OK)
        
        #Short polling
        new_messages = Message.objects.filter(timestamp__gt=last_polled
        ).select_related('client')
        
        if new_messages.exists():
            ClientLastPoll.objects.get(client=client).update_last_polled()
            serializer = MessageSerializer(new_messages, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response([], status=status.HTTP_200_OK)
                

class SSEMessagesView(APIView):
    """Server-Sent Events for streaming new messages."""
    
    def get(self, request):
        client_id = request.query_params.get('client_id')
        
        if not client_id:
            return Response(
                {'error': 'client_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            client = Client.objects.get(client_id=client_id)
        except Client.DoesNotExist:
            client = Client.objects.create(client_id=client_id)
            ClientLastPoll.objects.create(client=client)
            
        def event_stream():
            start_time = time.time()
            timeout = 3600  # 1 hour
            last_polled = ClientLastPoll.objects.get(client=client).last_polled
            
            while time.time() - start_time < timeout:
                new_messages = Message.objects.filter(
                    timestamp__gt=last_polled
                ).select_related('client')
                
                if new_messages.exists():
                    serializer = MessageSerializer(new_messages, many=True)
                    for message in serializer.data:
                        yield f"data: {json.dumps(message)}\n\n"
                    ClientLastPoll.objects.get(client=client).update_last_polled()
                    last_polled = timezone.now()
                
                time.sleep(1)  # Polling interval to avoid excessive CPU usage
                
        response = StreamingHttpResponse(
            event_stream(),
            content_type='text/event-stream'
        )
        response['Cache-Control'] = 'no-cache'
        # response['X-Accel-Buffering'] = 'no'  # Disable buffering in Nginx, if used
        return response