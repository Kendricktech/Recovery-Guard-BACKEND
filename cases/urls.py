from django.urls import path
from .views import CaseListApiView,CaseDetailView,CreateMoneyRecoveryApiView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('cases/',CaseListApiView.as_view(),name='case-list'),
    path('<int:pk>/',CaseDetailView.as_view(),name='case-detail'),
    path('money-recovery/', csrf_exempt(CreateMoneyRecoveryApiView.as_view()), name='money-recovery'),
    
]