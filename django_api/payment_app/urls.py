from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .webhooks import PaymentWebhook
from .views import OrderViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('payment/', PaymentWebhook.as_view(), name='payment-webhook'),
    path('', include(router.urls)),
]