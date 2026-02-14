from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from irctc.services import auth as auth_services
from irctc.services import train as train_services
from irctc.services import booking as booking_services
from irctc.serializers import auth as auth_serializers
from irctc.serializers import train as train_serializers
from irctc.serializers import booking as booking_serializers
from irctc.models import auth as auth_models
from irctc.models import train as train_models
from irctc.models import booking as booking_models

class RegisterView(APIView):
    """
    Register a new user
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = auth_serializers.RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': auth_serializers.UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    """
    Login with email and password
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = auth_serializers.LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

class UserDetailView(APIView):
    """
    Get current logged-in user details
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        return Response(auth_serializers.UserSerializer(request.user).data, status=status.HTTP_200_OK)

class TokenRefreshView(APIView):
    """
    Refresh access token using refresh token
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = auth_serializers.TokenRefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

class LogoutView(APIView):
    """
    Logout user by blacklisting refresh token
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response(
                    {'error': 'Refresh token is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            return Response(
                {'message': 'Logout successful'},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )