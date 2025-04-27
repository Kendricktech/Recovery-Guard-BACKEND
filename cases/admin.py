from django.contrib import admin
from .models import (
    Case,
    SupportingDocuments,
    CryptoLossReport,
    SocialMediaRecovery,
    MoneyRecoveryReport,
)


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'status', 'priority', 'agent', 'customer', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'agent__email', 'customer__email')
    list_filter = ('type', 'status', 'priority', 'is_closed', 'is_active')
    autocomplete_fields = ['agent', 'customer']


@admin.register(SupportingDocuments)
class SupportingDocumentsAdmin(admin.ModelAdmin):
    list_display = ('case', 'file', 'uploaded_at')
    list_filter = ('uploaded_at',)


@admin.register(CryptoLossReport)
class CryptoLossReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'crypto_type', 'amount_lost', 'sender_wallet', 'receiver_wallet', 'transaction_datetime')
    search_fields = ('title', 'sender_wallet', 'receiver_wallet', 'txid')


@admin.register(SocialMediaRecovery)
class SocialMediaRecoveryAdmin(admin.ModelAdmin):
    list_display = ('platform', 'username', 'email', 'submitted_at')
    search_fields = ('username', 'email', 'full_name')
    list_filter = ('platform', 'submitted_at')


@admin.register(MoneyRecoveryReport)
class MoneyRecoveryReportAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'amount', 'bank', 'datetime', 'submitted_at')
    search_fields = ('first_name', 'last_name', 'email', 'ref_number')
    list_filter = ('bank', 'submitted_at')


