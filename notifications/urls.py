# notifications/urls.py

from django.urls import path
from .views import NotificationListView  # this should be defined in views.py

urlpatterns = [
    path('notifications/', NotificationListView.as_view(), name='notification-list')
]
