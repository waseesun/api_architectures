from django.urls import path
from .views import WebhookReceiverView

urlpatterns = [
    path('webhook/', WebhookReceiverView.as_view(), name='webhook-receiver'),
]