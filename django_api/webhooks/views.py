import hmac
import hashlib
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import WebhookEvent
from .serializers import WebhookEventSerializer
from rest_api.models import Product

class WebhookReceiverView(APIView):
    def post(self, request):
        # Verify webhook signature (if provided)
        signature = request.headers.get('X-Webhook-Signature')
        if not self.verify_signature(request.body, signature):
            return Response({'error': 'Invalid signature'}, status=status.HTTP_401_UNAUTHORIZED)

        # Extract payload
        payload = request.data
        event_type = request.headers.get('X-Webhook-Event', 'unknown')

        # Process webhook (example: update product stock)
        product_id = payload.get('product_id')
        new_stock = payload.get('stock')
        product = None
        if product_id and new_stock is not None:
            try:
                product = Product.objects.get(id=product_id)
                product.stock = new_stock
                product.save()
            except Product.DoesNotExist:
                return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        # Save webhook event
        webhook_event = WebhookEvent.objects.create(
            event_type=event_type,
            payload=payload,
            product=product,
            processed=True
        )

        # Serialize and return response
        serializer = WebhookEventSerializer(webhook_event)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def verify_signature(self, payload, signature):
        if not signature:
            return False
        secret = os.getenv('WEBHOOK_SECRET', '').encode('utf-8')
        computed_signature = hmac.new(
            secret, payload, hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(computed_signature, signature)