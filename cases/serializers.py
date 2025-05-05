from rest_framework import serializers
from .models import Case, SocialMediaRecovery, MoneyRecoveryReport, CryptoLossReport
from django.utils.translation import gettext_lazy as _
import random


class CaseSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        # Handle user parameter for backward compatibility
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Store user in context if provided
        if user:
            self.context['user'] = user
    
    class Meta:
        model = Case
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
        # Mark customer as optional at the serializer level
        extra_kwargs = {
            'customer': {'required': False}
        }

    def create(self, validated_data):
        # Get the user either from context directly or from request
        user = self.context.get('user')
        if not user and 'request' in self.context:
            user = self.context['request'].user
        
        if user and hasattr(user, 'is_authenticated') and user.is_authenticated:
            # Set customer to the authenticated user
            validated_data['customer'] = user
        else:
            raise serializers.ValidationError({'customer': _('No authenticated user found to set as customer.')})
            
        # Set default title if not provided
        if not validated_data.get('title'):
            validated_data['title'] = f"Case-{random.randint(1, 10000)}"
            
        return super().create(validated_data)

    def validate(self, attrs):
        # Get the user either from context directly or from request
        user = self.context.get('user')
        if not user and 'request' in self.context:
            user = self.context['request'].user
            
        if user and hasattr(user, 'is_authenticated') and user.is_authenticated:
            # Set customer to the authenticated user
            attrs['customer'] = user
            
            # Set default title if not provided
            if not attrs.get('title'):
                attrs['title'] = f"Case-{random.randint(1, 10000)}"

        return attrs


class SocialMediaRecoverySerializer(CaseSerializer):
    class Meta(CaseSerializer.Meta):
        model = SocialMediaRecovery
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'type']

    def validate(self, attrs):
        attrs = super().validate(attrs)
        required_fields = ['platform', 'full_name', 'email', 'username']
        for field in required_fields:
            if not attrs.get(field):
                raise serializers.ValidationError({field: _(f'This field is required.')})
        return attrs

    def create(self, validated_data):
        validated_data['type'] = 'social_media'
        return super().create(validated_data)


class MoneyRecoveryReportSerializer(CaseSerializer):
    class Meta(CaseSerializer.Meta):
        model = MoneyRecoveryReport
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'type']

    def validate(self, attrs):
        attrs = super().validate(attrs)
        required_fields = ['first_name', 'last_name', 'phone', 'email', 'amount', 'bank', 'iban', 'datetime']
        for field in required_fields:
            if not attrs.get(field):
                raise serializers.ValidationError({field: _(f'This field is required.')})
        
        if attrs.get('amount') and attrs.get('amount') <= 0:
            raise serializers.ValidationError({'amount': _('Amount must be greater than zero.')})
        return attrs

    def create(self, validated_data):
        validated_data['type'] = 'money_recovery'
        return super().create(validated_data)


class CryptoLossSerializer(CaseSerializer):
    class Meta(CaseSerializer.Meta):
        model = CryptoLossReport
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'type']

    def validate(self, attrs):
        attrs = super().validate(attrs)
        required_fields = ['amount_lost', 'usdt_value', 'txid', 'sender_wallet', 
                          'receiver_wallet', 'crypto_type', 'transaction_datetime', 'loss_description']
        for field in required_fields:
            if not attrs.get(field):
                raise serializers.ValidationError({field: _(f'This field is required.')})
        
        # Handle mapping of frontend fields to model fields if needed
        if attrs.get('coin_type') and not attrs.get('crypto_type'):
            attrs['crypto_type'] = attrs.pop('coin_type')
            
        if attrs.get('transaction_hash') and not attrs.get('txid'):
            attrs['txid'] = attrs.pop('transaction_hash')
            
        return attrs

    def create(self, validated_data):
        validated_data['type'] = 'crypto'
        return super().create(validated_data)