# chat/signals.py

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from cases.models import Case
from accounts.models import CustomUser
from chat.models import Message
from notifications.models import Notification

# ---- Message Handling ----
@receiver(post_save, sender=Message)
def notify_new_message(sender, instance, created, **kwargs):
    if created and instance.receiver:
        Notification.objects.create(
            recipient=instance.receiver,
            message=f"New message from {instance.sender.email}",
            case=instance.case,
            message_obj=instance,
            notification_type='message'
        )

# Optional: notify sender when read (requires extra logic)

# ---- Case Handling ----
@receiver(post_save, sender=Case)
def notify_case_events(sender, instance, created, **kwargs):
    if created:
        if instance.agent:
            Notification.objects.create(
                recipient=instance.agent,
                message=f"You've been assigned to case '{instance.title}'",
                case=instance,
                notification_type='assignment'
            )
        if instance.customer:
            Notification.objects.create(
                recipient=instance.customer,
                message=f"Your case '{instance.title}' has been created.",
                case=instance,
                notification_type='case_created'
            )
    else:
        # Fetch previous version from DB
        old_instance = Case.objects.get(pk=instance.pk)

        changes = []
        if old_instance.status != instance.status:
            changes.append(f"Status changed to '{instance.status}'")
        if old_instance.priority != instance.priority:
            changes.append(f"Priority changed to '{instance.priority}'")
        if old_instance.agent != instance.agent:
            if instance.agent:
                Notification.objects.create(
                    recipient=instance.agent,
                    message=f"You’ve been assigned (or re-assigned) to case '{instance.title}'",
                    case=instance,
                    notification_type='reassignment'
                )
            if old_instance.agent:
                Notification.objects.create(
                    recipient=old_instance.agent,
                    message=f"You’ve been removed from case '{instance.title}'",
                    case=instance,
                    notification_type='unassignment'
                )
        if changes:
            note = "; ".join(changes)
            for user in [instance.agent, instance.customer]:
                if user:
                    Notification.objects.create(
                        recipient=user,
                        message=f"Case '{instance.title}' updated: {note}",
                        case=instance,
                        notification_type='case_update'
                    )

# ---- User Handling (Optional) ----
@receiver(post_save, sender=CustomUser)
def notify_user_signup(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            recipient=instance,
            message="Welcome! Your account has been created.",
            notification_type='account'
        )
