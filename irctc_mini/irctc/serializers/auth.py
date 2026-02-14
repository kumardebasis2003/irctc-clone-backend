from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from irctc.models import auth as auth_models

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = auth_models.User
        fields = ['id', 'name', 'email', 'role', 'date_joined']
        read_only_fields = ['id', 'role', 'date_joined']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, min_length=8, style={'input_type': 'password'})
    
    class Meta:
        model = auth_models.User
        fields = ['name', 'email', 'password', 'password_confirm']
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords do not match")
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = auth_models.User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    
    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        
        if not user.is_active:
            raise serializers.ValidationError('Account is disabled')
        
        refresh = RefreshToken.for_user(user)
        
        return {
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            'message': 'Login successful'
        }

class TokenRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    
    def validate(self, data):
        from rest_framework_simplejwt.serializers import TokenRefreshSerializer as BaseTokenRefreshSerializer
        serializer = BaseTokenRefreshSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    
    def validate(self, data):
        return data