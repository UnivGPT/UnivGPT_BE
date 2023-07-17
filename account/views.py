from django.shortcuts import render
import requests
from django.conf import settings

from django.contrib.auth.models import User
from .serializers import UserSerializer

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken

def set_token_on_response_cookie(user: User) -> Response:
    token = RefreshToken.for_user(user)
    user = User.objects.get(username=user)
    print("Found user", user)
    user_serializer = UserSerializer(user)
    res = Response(user_serializer.data, status=status.HTTP_200_OK)
    res.set_cookie('refresh_token', value=str(token))
    res.set_cookie('access_token', value=str(token.access_token))
    return res

# Create your views here.   
class SignupView(APIView):
    def post(self, request):
        email = request.data.get('email')
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
        refresh_token = request.data['refresh']
        try:
            RefreshToken(refresh_token).verify()
        except:
            return Response({"detail" : "로그인 후 다시 시도해주세요."}, status=status.HTTP_401_UNAUTHORIZED)
        new_access_token = str(RefreshToken(refresh_token).access_token)
        response = Response({"detail": "token refreshed"}, status=status.HTTP_200_OK)
        response.set_cookie('access_token', value=str(new_access_token))
        return response
    
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
        if request.data['email'] != user.email:
            return Response({"detail": "email should not be changed."}, status=status.HTTP_400_BAD_REQUEST)
        if not user_serializer.is_valid(raise_exception=True):
            return Response({"detail": "user data validation error"}, status=status.HTTP_400_BAD_REQUEST)
        user_serializer.save()
        return Response(user_serializer.data, status=status.HTTP_200_OK)

class SocialLoginCallbackView(APIView):
    def get(self, request):
        state = request.GET.get('state')
        code = request.GET.get('code')

        naver_client_id = settings.NAVER_CLIENT_ID
        naver_client_secret = settings.NAVER_SECRET_KEY
        
        token_url = f'https://nid.naver.com/oauth2.0/token?client_id={naver_client_id}&client_secret={naver_client_secret}&grant_type=authorization_code&state={state}&code={code}'
        
        print("================")
        response = requests.get(token_url)
        token_data = response.json()
        print("============")
        print("token type data:", type(token_data))


        headers = {
            'Authorization': f'Bearer {token_data.get("access_token")}'
        }

        print("============")
        print(type(token_data.get("access_token")))

        print(type(token_data["access_token"]))
        api_url = 'https://openapi.naver.com/v1/nid/me'
        api_response = Response(requests.get(api_url, headers=headers))

        print("api_response", api_response.data.json())

        return (Response(api_response.data.json(), status=status.HTTP_200_OK))
