from django.urls import path
from chat import views

urlpatterns = [
    # List all messages for the current user
    path('messages/', views.MessageListAPIView.as_view(), name='message-list'),
    
    # List all messages for a specific case
    path('case/<int:case_id>/messages/', views.CaseMessagesAPIView.as_view(), name='case-messages'),
    
    # Create a new message in a case
    path('case/<int:case_id>/send/', views.CreateMessageAPIView.as_view(), name='create-message'),
    
    # Get details of a message and mark as read if needed
    path('message/<int:pk>/', views.MessageDetailAPIView.as_view(), name='message-detail'),
]