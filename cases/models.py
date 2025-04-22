from django.db import models
from accounts.models import CustomUser

class Case(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    agent = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name='cases',
        limit_choices_to={'is_agent': True}
    )

    customer = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'is_customer': True}
    )

    status = models.CharField(max_length=50, default='open')
    priority = models.CharField(max_length=50, default='normal')
    resolution = models.TextField(blank=True, null=True)
    resolution_date = models.DateTimeField(blank=True, null=True)
    resolution_status = models.CharField(max_length=50, default='unresolved')

    def __str__(self):
        return self.title
    def get_images(self):
        return self.messages.filter(image__isnull=False)

    def get_documents(self):
        return self.messages.filter(document__isnull=False)

    def get_voice_notes(self):
        return self.messages.filter(voice_note__isnull=False)


class SupportingDocuments(models.Model):
    file = models.FileField(upload_to='supporting_documents/')
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='supporting_documents')
    uploaded_at = models.DateTimeField(auto_now_add=True)