from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status

from .models import Case
from .serializers import *

class CaseDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            case = Case.objects.get(pk=pk)

            if request.user != case.customer and (case.agent is None or case.agent != request.user):
                return Response({"error": "You do not have permission to view this case."}, status=status.HTTP_403_FORBIDDEN)

            if hasattr(case, 'cryptolossreport'):
                serializer = CryptoLossReportSerializer(case.cryptolossreport)
            elif hasattr(case, 'socialmediarecovery'):
                serializer = SocialMediaRecoverySerializer(case.socialmediarecovery)
            elif hasattr(case, 'moneyrecoveryreport'):
                serializer = MoneyRecoveryReportSerializer(case.moneyrecoveryreport)
            else:
                serializer = CaseSerializer(case)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Case.DoesNotExist:
            return Response({"error": "Case not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CaseListApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cases = Case.objects.filter(customer=request.user)
        serializer = CaseSerializer(cases, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateSocialMediaRecoveryApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        serializer = SocialMediaRecoverySerializer(
            data=request.data,
            context={'request': request, 'user': request.user}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateCryptoLossApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        serializer = CryptoLossSerializer(
            data=request.data,
            context={'request': request, 'user': request.user}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateMoneyRecoveryApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        serializer = MoneyRecoveryReportSerializer(
            data=request.data,
            context={'request': request, 'user': request.user}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
