from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from .models import CustomUser
from cases.models import Case
from chat.models import Message
from chat.views import MessageListAPIView


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



        

class CreateSuperUserApiView(APIView):
    def post(self, request):
        data = request.data
        email = data.get('email')
        password = data.get('password')

        if not all([email, password]):
            return JsonResponse(
                {'error': 'Email and password are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if CustomUser.objects.filter(email=email).exists():
            return JsonResponse(
                {'error': 'Email already exists.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = CustomUser.objects.create_superuser(
            email=email,
            password=password
        )

        return JsonResponse(
            {'message': f'Superuser {email} created successfully.'},
            status=status.HTTP_201_CREATED
        )


class LogoutApiView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()  # Requires `rest_framework_simplejwt.token_blacklist` enabled
            return JsonResponse({'message': 'Logout successful.'}, status=200)
        except Exception as e:
            return JsonResponse({'error': 'Invalid token or already blacklisted.'}, status=400)


from rest_framework.permissions import IsAdminUser

class UserListApiView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = CustomUser.objects.all().values('id', 'email', 'first_name', 'last_name', 'is_agent', 'is_customer')
        return JsonResponse(list(users), safe=False)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import JsonResponse
from rest_framework import status


class DashBoardApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        # Determine role
        is_agent = user.is_agent
        is_customer = user.is_customer

        # Fetch cases and messages relevant to the user
        if is_agent:
            cases = Case.objects.filter(agent=user)
        elif is_customer:
            cases = Case.objects.filter(customer=user)
        else:
            return JsonResponse({'error': 'User has no valid role.'}, status=status.HTTP_403_FORBIDDEN)

        messages = Message.objects.filter(sender=user) | Message.objects.filter(receiver=user)

        # Serialize cases
        cases_data = [
            {
                'id': case.id,
                'title': case.title,
                'description': case.description,
                'status': case.status,
                'priority': case.priority,
                'created_at': case.created_at.isoformat(),
                'updated_at': case.updated_at.isoformat(),
                'agent': case.agent.email if case.agent else None,
                'customer': case.customer.email,
                'resolution_status': case.resolution_status,
                'resolution_date': case.resolution_date.isoformat() if case.resolution_date else None,
            }
            for case in cases
        ]

        # Serialize messages
        messages_data = [
            {
                'id': message.id,
                'case_id': message.case.id,
                'subject': message.subject,
                'content': message.content,
                'sender': message.sender.email if message.sender else None,
                'receiver': message.receiver.email if message.receiver else None,
                'timestamp': message.timestamp.isoformat(),
                'is_read': message.is_read,
                'image': message.get_images(),
                'document': message.document.url if message.document else None,
                'voice_note': message.voice_note.url if message.voice_note else None,
            }
            for message in messages
        ]

        dashboard_data = {
            'stats': [
                {'label': 'Active Cases', 'value': cases.filter(status='active').count()},
                {'label': 'Resolved Cases', 'value': cases.filter(status='resolved').count()},
                {'label': 'Total Recovery', 'value': f"${sum(getattr(case, 'recovery_amount', 0) or 0 for case in cases)}"},
                {'label': 'Messages', 'value': messages.count()}
            ],
            'progress': {
                'steps': ['Submitted', 'Reviewing', 'In Progress', 'Finalizing', 'Resolved'],
                'currentStepIndex': 2  # Placeholder — later tie to actual case status
            },
            'activity': [
                {'icon': '📝', 'message': 'Case updated:', 'detail': 'ID#1234', 'time': '2 hrs ago'},
                {'icon': '💬', 'message': 'New message from agent', 'time': '5 hrs ago'},
                {'icon': '📄', 'message': 'Document uploaded:', 'detail': 'bank_statement.pdf', 'time': '1 day ago'},
                {'icon': '✅', 'message': 'Verification complete', 'time': '2 days ago'}
            ],
            'messages': messages_data,
            'cases': cases_data
        }

        return JsonResponse(dashboard_data, status=status.HTTP_200_OK, safe=False)
from django.contrib.auth.tokens import default_token_generator  
class PasswordRecoveryView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return JsonResponse({'error': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(email=email)
            # Here you would typically send an email with a password reset link
            return JsonResponse({'message': 'Password recovery email sent.'}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
   

# Class NotificationListView(ApiView):
#     pass
