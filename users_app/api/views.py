from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated

from .serializers import RegisterSerializer, LoginSerializer

User = get_user_model()


class RegisterView(APIView):
    """Handles user registration and returns an auth token on success."""

    def post(self, request):
        """Creates a new user and returns token and user information."""
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'fullname': user.fullname,
                'email': user.email,
                'user_id': user.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """Handles user login and returns an auth token on success."""

    def post(self, request):
        """Authenticates a user and returns token and user information."""
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'fullname': user.fullname,
                'email': user.email,
                'user_id': user.id
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailCheckView(APIView):
    """Checks if an email address is already registered."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Returns user info if the email exists, 404 if not."""
        email = request.query_params.get('email')
        if not email:
            return Response(
                {'error': 'Email parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            user = User.objects.get(email=email)
            return Response({
                'id': user.id,
                'email': user.email,
                'fullname': user.fullname
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(
                {'error': 'Email not found'},
                status=status.HTTP_404_NOT_FOUND
            )
