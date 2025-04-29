from django.urls import path
from .views import CreateAgentApiView, CreateCustomerApiView, UserListApiView, LoginApiView, DashBoardApiView, EmailLeadsApiView, CreateEmailLeadApiView

urlpatterns = [
    path('create-agent/', CreateAgentApiView.as_view(), name='create_agent'),
    path('create-customer/', CreateCustomerApiView.as_view(), name='create_customer'),
    path('user-list/', UserListApiView.as_view(), name='user_list'),
    path('login/', LoginApiView.as_view(), name='login'),
    path('dashboard/', DashBoardApiView.as_view(), name='dashboard'),
    path('email-leads/', EmailLeadsApiView.as_view(), name='email_leads'),
    path('create-email-lead/', CreateEmailLeadApiView.as_view(), name='create_email_lead'),
]
