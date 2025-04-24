from rest_framework import serializers
from .models import Case, CryptoLossReport, SocialMediaRecovery, MoneyRecoveryReport

class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = ['id', 'title', 'description', 'status', 'priority', 'created_at', 'updated_at']

class CryptoLossReportSerializer(CaseSerializer):
    class Meta:
        model = CryptoLossReport
        fields = CaseSerializer.Meta.fields + [
            'amount_lost', 'usdt_value', 'txid', 'sender_wallet', 'receiver_wallet', 
            'platform_used', 'blockchain_hash', 'payment_method', 'crypto_type', 'transaction_datetime', 'loss_description'
        ]

class SocialMediaRecoverySerializer(CaseSerializer):
    class Meta:
        model = SocialMediaRecovery
        fields = CaseSerializer.Meta.fields + [
            'platform', 'username', 'profile_url', 'profile_pic', 'submitted_at'
        ]

class MoneyRecoveryReportSerializer(CaseSerializer):
    class Meta:
        model = MoneyRecoveryReport
        fields = CaseSerializer.Meta.fields + [
            'first_name', 'last_name', 'phone', 'email', 'amount', 'ref_number', 
            'bank', 'iban', 'datetime', 'submitted_at'
        ]
