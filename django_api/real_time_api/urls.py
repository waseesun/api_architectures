from django.urls import path
from . import views

urlpatterns = [
    path('send-message/', views.SendMessageView.as_view(), name='send-message'),
    path('poll-messages/', views.PollMessagesView.as_view(), name='poll-messages'),
    path('sse-messages/', views.SSEMessagesView.as_view(), name='sse-messages'),
]