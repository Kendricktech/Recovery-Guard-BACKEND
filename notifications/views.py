# notifications/views.py (example)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Notification

class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')[:50]
        return Response([{
            'message': n.message,
            'created_at': n.created_at,
            'is_read': n.is_read,
            'type': n.notification_type
        } for n in notifications])
