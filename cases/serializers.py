from rest_framework import serializers
from .models import Case, SocialMediaRecovery, MoneyRecoveryReport
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
        # Debug print to check what's in context
        print(f"Context in create: {self.context}")
        
        # Get the user either from context directly or from request
        user = self.context.get('user')
        if not user and 'request' in self.context:
            user = self.context['request'].user
        
        print(f"User found: {user}")
        
        if user and hasattr(user, 'is_authenticated') and user.is_authenticated:
            # Set customer to the authenticated user
            validated_data['customer'] = user
            print(f"Setting customer to: {user}")
        else:
            print("No valid user found in context")
            
        # Make sure customer is set before creating
        if not validated_data.get('customer'):
            raise serializers.ValidationError({'customer': _('No authenticated user found to set as customer.')})
            
        return super().create(validated_data)

    def validate(self, attrs):
        # Debug print to check what's in context during validation
        print(f"Context in validate: {self.context}")
        
        # Get the user either from context directly or from request
        user = self.context.get('user')
        if not user and 'request' in self.context:
            user = self.context['request'].user

                    
        print(f"User in validate: {user}")
            
        if user and hasattr(user, 'is_authenticated') and user.is_authenticated:
            # Set customer to the authenticated user
            attrs['customer'] = user
            print(f"Setting customer in validate to: {user}")
            attrs['title']= random_ref = random.randint(1, 1000)


        return attrs


class SocialMediaRecoverySerializer(CaseSerializer):
    class Meta(CaseSerializer.Meta):
        model = SocialMediaRecovery
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'type']

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if not attrs.get('platform'):
            raise serializers.ValidationError({'platform': _('This field is required.')})
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
        if not attrs.get('amount') or attrs.get('amount') <= 0:
            raise serializers.ValidationError({'amount': _('Amount must be greater than zero.')})
        return attrs

    def create(self, validated_data):
        validated_data['type'] = 'money_recovery'
        return super().create(validated_data)