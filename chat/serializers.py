from rest_framework import serializers
from chat.models import Message
from accounts.models import CustomUser
from cases.models import Case

class UserBasicSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'full_name']
    
    def get_full_name(self, obj):
        if hasattr(obj, 'first_name') and hasattr(obj, 'last_name'):
            return f"{obj.first_name} {obj.last_name}".strip() or obj.email
        return obj.email

class MessageSerializer(serializers.ModelSerializer):
    sender_details = UserBasicSerializer(source='sender', read_only=True)
    receiver_details = UserBasicSerializer(source='receiver', read_only=True)
    case_title = serializers.CharField(source='case.title', read_only=True)
    attachment_type = serializers.SerializerMethodField()
    
    class Meta:
        model = Message
        fields = [
            'id', 'case', 'sender', 'receiver', 'subject', 'content',
            'image', 'document', 'voice_note', 'timestamp', 'is_read',
            'sender_details', 'receiver_details', 'case_title', 'attachment_type'
        ]
        read_only_fields = ['id', 'timestamp', 'is_read']
    
    def get_attachment_type(self, obj):
        if obj.image:
            return 'image'
        elif obj.document:
            return 'document'
        elif obj.voice_note:
            return 'voice_note'
        return None
    
    def validate(self, data):
        # Make sure sender and receiver are not the same
        if data.get('sender') == data.get('receiver'):
            raise serializers.ValidationError("Cannot send message to yourself")
        
        # Ensure the sender has access to the specified case
        case = data.get('case')
        sender = self.context['request'].user
        if case and not Case.objects.filter(id=case.id).filter(
            models.Q(client=sender) | models.Q(lawyer=sender) | models.Q(admin=sender)
        ).exists():
            raise serializers.ValidationError("You don't have access to this case")
        
        return data