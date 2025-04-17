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
    pass

class CreateSuperUserApiView(APIView):
    pass

class LoginApiView(APIView):
    pass

class LogoutApiView(APIView):
    pass

class UserListApiView(APIView):
    pass
