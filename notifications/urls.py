# notifications/urls.py

from django.urls import path
from .views import NotificationListView,UnreadCountView # this should be defined in views.py

urlpatterns = [
    path('', NotificationListView.as_view(), name='notification-list'),
        path("count/", UnreadCountView.as_view(), name="notification-count"),

]
