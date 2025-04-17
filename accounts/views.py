from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from .models import CustomUser

class CreateAgentApiView(APIView):
    def post(self, request):
        data = request.data
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')
        username = data.get('username', '')

        if not all([email, password]):
            return JsonResponse(
                {'error': 'Email and password are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if CustomUser.objects.filter(email=email).exists():
            return JsonResponse(
                {'error': 'Email already exists for another user.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create user with provided information
        user = CustomUser.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            username=username,
            is_agent=True,
            is_customer=False
        )

        # Return success message
        full_name = f"{first_name} {last_name}" if not username else username
        return JsonResponse(
            {'message': f'Agent {full_name} ({email}) created successfully.'},
            status=status.HTTP_201_CREATED
        )


class CreateCustomerApiView(APIView):
    def post(self, request):
        data = request.data
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')
        username = data.get('username', '')

        if not all([email, password]):
            return JsonResponse(
                {'error': 'Email and password are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if CustomUser.objects.filter(email=email).exists():
            return JsonResponse(
                {'error': 'Email already exists for another user.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create user with provided information
        user = CustomUser.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            username=username,
            is_agent=False,
            is_customer=True
        )

        # Return success message
        full_name = f"{first_name} {last_name}" if not username else username
        return JsonResponse(
            {'message': f'Customer {full_name} ({email}) created successfully.'},
            status=status.HTTP_201_CREATED
        )


class CreateSuperUserApiView(APIView):
    pass

from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from accounts.models import CustomUser  # if needed

class LoginApiView(APIView):
    def post(self, request):
        data = request.data
        email = data.get('email')
        password = data.get('password')

        if not all([email, password]):
            return JsonResponse(
                {'error': 'Email and password are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(request, email=email, password=password)

        if user is None:
            return JsonResponse(
                {'error': 'Invalid credentials.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)

        return Response({
            'message': 'Login successful.',
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)


class LogoutApiView(APIView):
    pass

class UserListApiView(APIView):
    pass
