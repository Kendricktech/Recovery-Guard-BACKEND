from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import (
    CaseListApiView,
    CaseDetailView,
    CreateMoneyRecoveryApiView,
    CreateCryptoLossApiView,
    CreateSocialMediaRecoveryApiView,
)

urlpatterns = [
    # Case endpoints
    path('cases/', CaseListApiView.as_view(), name='case-list'),
    path('cases/<int:pk>/', CaseDetailView.as_view(), name='case-detail'),

    # Recovery submission endpoints
    path('money-recovery/', csrf_exempt(CreateMoneyRecoveryApiView.as_view()), name='money-recovery'),
    path('crypto-recovery/', csrf_exempt(CreateCryptoLossApiView.as_view()), name='crypto-recovery'),
    path('social-media-recovery/', csrf_exempt(CreateSocialMediaRecoveryApiView.as_view()), name='social-media-recovery'),
]
