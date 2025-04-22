# notifications/models.py

from django.db import models
from accounts.models import CustomUser
from cases.models import Case
from chat.models import Message

class Notification(models.Model):
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    case = models.ForeignKey(Case, on_delete=models.CASCADE, null=True, blank=True)
    message_obj = models.ForeignKey(Message, on_delete=models.CASCADE, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.recipient.email}: {self.message}"
