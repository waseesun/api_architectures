from django.db import models
from rest_api.models import Product

class WebhookEvent(models.Model):
    event_type = models.CharField(max_length=100)  # e.g., 'product.stock_updated'
    payload = models.JSONField()  # Store raw payload
    received_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.event_type} - {self.received_at}"