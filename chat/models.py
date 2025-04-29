from django.core.validators import FileExtensionValidator
from django.db import models
from cases.models import Case
from accounts.models import CustomUser
class Message(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True,blank=True , related_name='sent_messages')
    receiver = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True,blank=True, related_name='received_messages')
    subject = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True)
    
    image = models.ImageField(
        upload_to='chat/images/',
        blank=True,
        null=True
    )
    
    document = models.FileField(
        upload_to='chat/documents/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'docx', 'xlsx', 'pptx', 'txt'])]
    )

    voice_note = models.FileField(
        upload_to='chat/voice_notes/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['mp3', 'wav', 'ogg'])]
    )

    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def get_images(self):
        return self.image.url if self.image else None

    def __str__(self):
        return f"Message from {self.sender.email} in case '{self.case.title}'"

