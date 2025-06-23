from django.urls import path, re_path
from . import views
from . import websockets

urlpatterns = [
    path('send-message/', views.SendMessageView.as_view(), name='send-message'),
    path('poll-messages/', views.PollMessagesView.as_view(), name='poll-messages'),
    path('sse-messages/', views.SSEMessagesView.as_view(), name='sse-messages'),
]

websocket_urlpatterns = [
    re_path(r'ws/messages/(?P<client_id>[0-9a-f-]+)/$', websockets.WebSocketMessageConsumer.as_asgi()),
]