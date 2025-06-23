"""
Views for short and long polling, SSE (Server-Sent Events) and WebSockets.
"""
import json, time, asyncio, logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import StreamingHttpResponse
from django.utils import timezone
from adrf.views import APIView as AdrfAPIView
from asgiref.sync import sync_to_async
from django_api.renderers import ViewRenderer, SSERenderer
from .models import Client, Message, ClientLastPoll
from .serializers import MessageSerializer


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
                

class SSEMessagesView(AdrfAPIView):
    """Server-Sent Events for streaming new messages."""
    renderer_classes = [SSERenderer]
    
    async def get(self, request):
        # No wrapping needed because it is fast enough
        client_id = request.query_params.get('client_id')

        if not client_id:
            return Response(
                {'error': 'client_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Use sync_to_async for synchronous ORM operations
        try:
            # sync object wrapped into async function and then arguments are passed
            client = await sync_to_async(Client.objects.get)(client_id=client_id)
        except Client.DoesNotExist:
            client = await sync_to_async(Client.objects.create)(client_id=client_id)
            await sync_to_async(ClientLastPoll.objects.create)(client=client)

        async def event_stream():
            try:
                start_time = time.time()
                timeout = 3600  # 1 hour
                # Get last_polled asynchronously
                last_polled_obj = await sync_to_async(ClientLastPoll.objects.get)(client=client)
                last_polled = last_polled_obj.last_polled

                while time.time() - start_time < timeout:
                    # Fetch new messages asynchronously
                    new_messages = await sync_to_async(
                        lambda: Message.objects.filter(timestamp__gt=last_polled).select_related('client')
                    )()

                    # Check if new messages exist asynchronously
                    if await sync_to_async(new_messages.exists)():
                        # Serialize messages asynchronously, including data access
                        serializer = MessageSerializer(new_messages, many=True)
                        # Access serializer.data within sync_to_async
                        serialized_data = await sync_to_async(lambda: serializer.data)()
                        for message in serialized_data:
                            yield f"data: {json.dumps(message)}\n\n"
                        # Update last_polled asynchronously
                        await sync_to_async(last_polled_obj.update_last_polled)()
                        last_polled = timezone.now()

                    # Non-blocking sleep
                    await asyncio.sleep(1)
            except asyncio.CancelledError:
                print(f"Client {client_id} disconnected")
                raise  # Polling interval to avoid excessive CPU usage
                
        response = StreamingHttpResponse(
            event_stream(),
            content_type='text/event-stream'
        )
        response['Cache-Control'] = 'no-cache' # Disable caching because real time data is dynamic
        # response['X-Accel-Buffering'] = 'no'  # Disable buffering in Nginx, if used
        return response
