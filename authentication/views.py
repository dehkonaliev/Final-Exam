from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from .utils import success_response, error_response
from .serializers import (
    TempUserSerializer, VerifyCodeSerializer,
    CreateAccountSerializer, LoginSerializer,
    LogoutSerializer, UserUpdateSettingsSerializer,
    ChangePasswordSerializer,
)
from rest_framework_simplejwt.tokens import RefreshToken

class CreateTempUserAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = TempUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return success_response(message="Temp user created", data=serializer.data, status_code=201)
    

class VerifyCodeAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return success_response(message="Code verified", data=serializer.data, status_code=201)
    

class CreateAccountAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CreateAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return success_response(message="Account created", data=serializer.data, status_code=201)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)

        return success_response(
            message="Login successful",
            data={
                'user': {
                    'id': str(user.id),
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                },
                'tokens': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                },
            },
            status_code=200,
        )


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return success_response(message="Logged out successfully", status_code=200)


class UpdateSettingsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def patch(self, request):
        serializer = UserUpdateSettingsSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_response(message="Settings updated", data=serializer.data)
    
class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_response(message="Password changed successfully", status_code=200)