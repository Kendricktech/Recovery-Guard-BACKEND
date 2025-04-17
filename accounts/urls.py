from django.urls import path
from .views import CreateAgentApiView,CreateCustomerApiView,UserListApiView

urlpatterns=[
    path('create-agent/', CreateAgentApiView.as_view(), name='create_agent'),
    path('create-customer/', CreateCustomerApiView.as_view(), name='create_customer'),
    path('user-list/', UserListApiView.as_view(), name='user_list'),
]