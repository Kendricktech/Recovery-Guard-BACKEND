from django.urls import path
from .views import CreateAgentApiView,CreateCustomerApiView,UserListApiView ,LoginApiView,DashBoardApiView

urlpatterns=[
    path('create-agent/', CreateAgentApiView.as_view(), name='create_agent'),
    path('create-customer/', CreateCustomerApiView.as_view(), name='create_customer'),
    path('user-list/', UserListApiView.as_view(), name='user_list'),
    path('login/', LoginApiView.as_view(), name='login'),
    path('dashboard/', DashBoardApiView.as_view(), name='dashboard'),
]