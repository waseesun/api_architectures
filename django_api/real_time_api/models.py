from django.db import models
from django.utils import timezone
import uuid

class Client(models.Model):
    """
    Represents a client (no login required, just a unique ID).
    """
    client_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Client {self.client_id}"

class Message(models.Model):
    """
    Represents a message in the system.
    """
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='messages', null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['timestamp']
        indexes = [
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return f"Message from {self.client.client_id if self.client else 'Anonymous'} at {self.timestamp}"

class ClientLastPoll(models.Model):
    """
    Tracks the last time a client polled for new messages.
    """
    client = models.OneToOneField(Client, on_delete=models.CASCADE, related_name='last_poll')
    last_polled = models.DateTimeField(default=timezone.now)

    def update_last_polled(self):
        """
        Updates the last polled timestamp.
        """
        self.last_polled = timezone.now()
        self.save()

    def __str__(self):
        return f"Client {self.client.client_id} last polled at {self.last_polled}"