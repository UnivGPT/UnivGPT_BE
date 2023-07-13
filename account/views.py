from django.shortcuts import render
from .models import User
from .serializers import UserSerializer

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

def set_token_on_response_cookie(user: User) -> Response:
    token = RefreshToken.for_user(user)
    user = User.objects.get(user=user)
    user_serializer = UserSerializer(user)
    res = Response(user_serializer.data, status=status.HTTP_200_OK)
    res.set_cookie('refresh_token', value=str(token), httponly=True)
    res.set_cookie('access_token', value=str(token.access_token), httponly=True)
    return res

# Create your views here.
class SignupView(APIView):
    def post(self, request):
        user_serializer = UserSerializer(data = request.data)
        if user_serializer.is_valid(raise_exception=True):
            user = user_serializer.save()
        return set_token_on_response_cookie(user)
    
class SignupView(APIView):
    def post(self, request):
        email = request.data.get('email', '')
        username = email.split('@')[0]  # 이메일에서 @ 앞부분을 사용하여 사용자 이름 생성

        # request.data에 username 추가
        request.data['username'] = username

        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid(raise_exception=True):
            user = user_serializer.save()
        return set_token_on_response_cookie(user)

    
class SigninView(APIView):
    def post(self, request):
        try:
            user = User.objects.get(
                email = request.data['email'],
                password = request.data['password']
            )
        except:
            return Response({"detail": "이메일 또는 비밀번호를 확인해주세요."}, status=status.HTTP_400_BAD_REQUEST)
        return set_token_on_response_cookie(user)

class LogoutView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "로그인 후 다시 시도해주세요."}, status=status.HTTP_401_UNAUTHORIZED)
        RefreshToken(request.data['refresh']).blacklist()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class TokenRefreshView(APIView):
    def post(self, request):
        is_access_token_valid = request.user.is_authenticated
        refresh_token = request.data['refresh']
        try:
            RefreshToken(refresh_token).verify()
            is_refresh_token_blacklisted = True
        except:
            is_refresh_token_blacklisted = False
        
        if not is_access_token_valid:
            if not is_refresh_token_blacklisted:
                return Response({"detail": "login을 다시 해주세요."}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                new_access_token = str(RefreshToken(refresh_token).access_token)
        else:
            user = request.user
            token = AccessToken.for_user(user)
            new_access_token = str(token)
        response = Response({"detail": "token refreshed"}, status=status.HTTP_200_OK)
        return response.set_cookie('access_token', value=str(new_access_token), httponly=True)
    
class UserInfoView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "로그인 후 다시 시도해주세요."}, status=status.HTTP_401_UNAUTHORIZED)
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request):
        user = request.user
        user_serializer = UserSerializer(user, data=request.data, partial=True)
        if not user_serializer.is_valid(raise_exception=True):
            return Response({"detail": "user data validation error"}, status=status.HTTP_400_BAD_REQUEST)
        user_serializer.save()
        return Response(user_serializer.data, status=status.HTTP_200_OK)