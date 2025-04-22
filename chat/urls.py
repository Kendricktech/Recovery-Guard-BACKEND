from django.urls import path
from .views import MessageListAPIView

urlpatterns = [
    path('messages', MessageListAPIView.as_view(), name='message-list'),    
]