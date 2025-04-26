from django.urls import path
from .views import CaseListApiView,CaseDetailView,CreateCryptoLossAPIView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('cases/',CaseListApiView.as_view(),name='case-list'),
    path('<int:pk>/',CaseDetailView.as_view(),name='case-detail'),
    
    path('crypto-loss',CreateCryptoLossAPIView.as_view(), name='crypto-loss'),
    
]