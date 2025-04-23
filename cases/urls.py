from django.urls import path
from .views import CaseListApiView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('cases/',CaseListApiView.as_view(),name='case-list'),
    
]