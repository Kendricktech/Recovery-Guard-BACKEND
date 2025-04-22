from django.shortcuts import render
from rest_framework.views import APIView
# Create your views here.
class CaseListApiView(APIView):
    def get(self, request):
        # Logic to retrieve and return a list of cases
        pass
class CreateCryptoLossAPIView(APIView):
    def post(self, request):
        data = request.data
        