from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from django.db.models import Q
from chat.models import Message
from chat.serializers import MessageSerializer
from cases.models import Case
from django.shortcuts import get_object_or_404

class MessageListAPIView(ListAPIView):
    """List all messages for the current user (sent and received)"""
    serializer_class = MessageSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(
            Q(sender=user) | Q(receiver=user)
        ).order_by('-timestamp')

class CaseMessagesAPIView(ListAPIView):
    """List all messages for a specific case"""
    serializer_class = MessageSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        case_id = self.kwargs['case_id']
        user = self.request.user
        
        # Verify user has access to this case
        case = get_object_or_404(Case, id=case_id)
        if not Case.objects.filter(
            id=case_id
        ).filter(
            Q(customer=user) | Q(agent=user) 
        ).exists():
            return Message.objects.none()
            
        return Message.objects.filter(case_id=case_id).order_by('timestamp')

class CreateMessageAPIView(APIView):
    """Create a new message in a case"""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, case_id):
        try:
            case = Case.objects.get(id=case_id)
            
            # Check if user has access to the case
            user = request.user
            if not Case.objects.filter(
                id=case_id
            ).filter(
                Q(agent=user) | Q(customer=user) 
            ).exists():
                return Response(
                    {"detail": "You don't have access to this case."}, 
                    status=status.HTTP_403_FORBIDDEN
                )
                
        except Case.DoesNotExist:
            return Response(
                {"detail": "Case not found."}, 
                status=status.HTTP_404_NOT_FOUND
            )

        data = request.data.copy()
        data['case'] = case.id
        data['sender'] = request.user.id
        
        # Determine receiver automatically based on case and sender
        if case.lawyer and case.lawyer != user:
            data['receiver'] = case.lawyer.id
        elif case.client and case.client != user:
            data['receiver'] = case.client.id
        
        serializer = MessageSerializer(
            data=data, 
            context={'request': request}
        )
        
        if serializer.is_valid():
            message = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MessageDetailAPIView(RetrieveUpdateAPIView):
    """Get details of a specific message or mark as read"""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer
    
    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(
            Q(sender=user) | Q(receiver=user)
        )
    
    def get_object(self):
        obj = super().get_object()
        # Mark message as read if receiving user is accessing it
        if self.request.user == obj.receiver and not obj.is_read:
            obj.is_read = True
            obj.save()
        return obj