from django.db import models
from accounts.models import CustomUser

class Case(models.Model):
    TYPE_CHOICES = [
        ('general', 'General'),
        ('crypto', 'Crypto'),
        ('money_recovery', 'Money Recovery'),
        ('social_media', 'Social Media'),
    ]
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
    is_active = models.BooleanField(default=True)
    is_closed = models.BooleanField(default=False)
    type = models.CharField(max_length=50, default='general')
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



from django.db import models

class CryptoLossReport(Case):
    def save(self, *args, **kwargs):
        self.type = 'crypto'
        super().save(*args, **kwargs)

    crypto_choices = [
        ("Bitcoin", "Bitcoin"),
        ("Ethereum", "Ethereum"),
        ("USDT", "USDT"),
        ("BNB", "BNB"),
        ("Solana", "Solana"),
        ("Other", "Other"),
    ]

    amount_lost = models.DecimalField(max_digits=20, decimal_places=8)
    usdt_value = models.DecimalField(max_digits=20, decimal_places=8)
    txid = models.CharField(max_length=255)
    sender_wallet = models.CharField(max_length=255)
    receiver_wallet = models.CharField(max_length=255)
    platform_used = models.CharField(max_length=255, blank=True, null=True)
    blockchain_hash = models.CharField(max_length=255, blank=True, null=True)
    payment_method = models.CharField(max_length=255, blank=True, null=True)
    exchange_info = models.TextField(blank=True, null=True)
    wallet_backup = models.TextField(blank=True, null=True)
    crypto_type = models.CharField(max_length=50, choices=crypto_choices, default="Bitcoin")
    transaction_datetime = models.DateTimeField()
    loss_description = models.TextField()



class SocialMediaRecovery(Case):
    type='social_media'
    PLATFORM_CHOICES = [
        ("Facebook", "Facebook"),
        ("Instagram", "Instagram"),
        ("Twitter", "Twitter"),
        ("LinkedIn", "LinkedIn"),
        ("Snapchat", "Snapchat"),
        ("TikTok", "TikTok"),
        ("Reddit", "Reddit"),
        ("YouTube", "YouTube"),
        ("Pinterest", "Pinterest"),
        ("WhatsApp", "WhatsApp"),
        ("Telegram", "Telegram"),
        ("Other", "Other"),
    ]

    platform = models.CharField(max_length=30, choices=PLATFORM_CHOICES)
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    username = models.CharField(max_length=150)
    profile_url = models.URLField(blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.platform} - {self.username}"


from django.db import models
from django.contrib.auth import get_user_model

class MoneyRecoveryReport(Case):
    type = 'money_recovery'
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    identification = models.CharField(max_length=150)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    ref_number = models.CharField(max_length=150, blank=True, null=True)
    bank = models.CharField(max_length=150)
    iban = models.CharField(max_length=150)
    datetime = models.DateTimeField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.amount} lost"

class MoneyRecoveryFile(models.Model):
    report = models.ForeignKey(MoneyRecoveryReport, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='money_recovery_files/')
