from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import JsonResponse
from rest_framework import status

# CreatSe your views here.
class CaseListApiView(APIView):
    def get(self, request):
        # Logic to retrieve and return a list of cases
        pass
class CreateCryptoLossAPIView(APIView):
    def post(self, request):
        data = request.data
        
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Case, CryptoLossReport, SocialMediaRecovery, MoneyRecoveryReport
from .serializers import CaseSerializer, CryptoLossReportSerializer, SocialMediaRecoverySerializer, MoneyRecoveryReportSerializer

class CaseDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        # First check if user is authenticated
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required"}, status=401)
            
        try:
            # Fetch the base case first
            case = Case.objects.get(pk=pk)

            # Check permissions
            if request.user != case.customer and (case.agent is None or case.agent != request.user):
                return Response({"error": "You do not have permission to view this case."}, status=403)

            # Try to get the specific case type
            try:
                if hasattr(case, 'cryptolossreport'):
                    specific_case = case.cryptolossreport
                    serializer = CryptoLossReportSerializer(specific_case)
                elif hasattr(case, 'socialmediarecovery'):
                    specific_case = case.socialmediarecovery
                    serializer = SocialMediaRecoverySerializer(specific_case)
                elif hasattr(case, 'moneyrecoveryreport'):
                    specific_case = case.moneyrecoveryreport
                    serializer = MoneyRecoveryReportSerializer(specific_case)
                else:
                    # Fall back to the base case serializer if no specific type is found
                    serializer = CaseSerializer(case)
            except Exception as e:
                # If there's any error getting the specific type, use the base serializer
                serializer = CaseSerializer(case)

            return Response(serializer.data, status=200)
        except Case.DoesNotExist:
            return Response({"error": "Case not found"}, status=404)
        except Exception as e:
            # Generic catch-all for any other exceptions
            return Response({"error": f"An error occurred: {str(e)}"}, status=500)