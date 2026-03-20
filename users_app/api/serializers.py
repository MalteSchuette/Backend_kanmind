# serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration. Validates and creates a new user."""

    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['fullname', 'email', 'password', 'repeated_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        """Checks that both passwords match."""
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        """Creates a new user with a hashed password."""
        validated_data.pop('repeated_password')
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    """Serializer for user login. Validates email and password credentials."""

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """Authenticates the user and attaches the user object to the validated data."""
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        data['user'] = user
        return data
