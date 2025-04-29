# chat/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from cases.models import Case
from accounts.models import CustomUser
from .models import Message ,Notification

@receiver(post_save, sender=Message)
def notify_on_new_message(sender, instance, created, **kwargs):
    if created and instance.receiver:
        Notification.objects.create(
            recipient=instance.receiver,
            message=f"New message from {instance.sender.email}",
            case=instance.case,
            message_obj=instance
        )

@receiver(post_save, sender=Case)
def notify_on_case_assignment(sender, instance, created, **kwargs):
    if created and instance.agent:
        Notification.objects.create(
            recipient=instance.agent,
            message=f"You have been assigned to case '{instance.title}'",
            case=instance
        )
def notify_on_case_update(sender, instance, **kwargs):
    if instance.agent:
        Notification.objects.create(
            recipient=instance.agent,
            message=f"Case '{instance.title}' has been updated",
            case=instance
        )
z