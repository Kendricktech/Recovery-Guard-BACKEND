from django.shortcuts import render
from rest_framework.views import APIView
# CreatSe your views here.
class CaseListApiView(APIView):
    def get(self, request):
        # Logic to retrieve and return a list of cases
        pass
class CreateCryptoLossAPIView(APIView):
    def post(self, request):
        data = request.data
        
class CaseDetailView(APIView):
    def get(self, request, case_id):
        # Logic to retrieve and return details of a specific case
        pass