from django.shortcuts import render, redirect
import requests, os

from django.conf import settings
from json import JSONDecodeError
from django.http import JsonResponse
from django.contrib.auth.models import User
from .serializers import UserSerializer

import random
import string

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken

import random
import string

def set_token_on_response_cookie(user: User) -> Response:
    token = RefreshToken.for_user(user)
    user = User.objects.get(username=user)
    print("Found user", user)
    user_serializer = UserSerializer(user)
    res = Response(user_serializer.data, status=status.HTTP_200_OK)
    res.set_cookie('refresh_token', value=str(token))
    res.set_cookie('access_token', value=str(token.access_token))
    return res

def generate_random_string(length=8):
    characters = string.ascii_letters + string.digits + string.punctuation
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

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
        
        response = requests.get(token_url)
        token_data = response.json()

        headers = {
            'Authorization': f'Bearer {token_data.get("access_token")}'
        }

        api_url = 'https://openapi.naver.com/v1/nid/me'
        api_response = Response(requests.get(api_url, headers=headers))

        user_profile = api_response.data.json().get('response')
        print(user_profile)

        email = user_profile.get("email")

        try:
            user = User.objects.get(email=email)
            print("existing user using social login")
            return set_token_on_response_cookie(user)
        except:
            username = email.split('@')[0]
            password = generate_random_string()

            data = {
                "email": email,
                "username": username,
                "password": password,
            }

            user_serializer = UserSerializer(data=data)
            if user_serializer.is_valid(raise_exception=True):
                user = user_serializer.save()
            return set_token_on_response_cookie(user)
        api_url = 'https://openapi.naver.com/v1/nid/me'
        api_response = Response(requests.get(api_url, headers=headers))

        return (Response(api_response.data.json(), status=status.HTTP_200_OK))

class KakaoLoginCallbackView(APIView):
    def get(self, request):
        code = request.GET.get('code')

        kakao_client_id = settings.KAKAO_CLIENT_ID
        kakao_client_secret = settings.KAKAO_SECRET_KEY
        kakao_redirect_uri = settings.KAKAO_REDIRECT_URI
        
        token_url = f'https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={kakao_client_id}&client_secret={kakao_client_secret}&code={code}&redirect_uri={kakao_redirect_uri}'
        
        response = requests.get(token_url)
        token_data = response.json()

      


        headers = {
            'Authorization': f'Bearer {token_data.get("access_token")}',
            'Content-type': "application/x-www-form-urlencoded;charset=utf-8"
        }


        api_url = 'https://kapi.kakao.com/v2/user/me'
        api_response = Response(requests.get(api_url, headers=headers))

        print("api_response", api_response.data.json())

        user_profile = api_response.data.json().get('kakao_account')

        email = user_profile.get("email")


        try:
            user = User.objects.get(email=email)
            print("existing user using social login")
            return set_token_on_response_cookie(user)
        except:
            username = email.split('@')[0]
            password = generate_random_string()

            data = {
                "email": email,
                "username": username,
                "password": password,
            }

            user_serializer = UserSerializer(data=data)
            if user_serializer.is_valid(raise_exception=True):
                user = user_serializer.save()
            return set_token_on_response_cookie(user)



class GoogleLoginView(APIView):
    def get(self, request):
        client_id = settings.GOOGLE_CLIENT_ID
        client_secret = settings.GOOGLE_SECRET
        redirect_uri = settings.GOOGLE_REDIRECT_URI
        code = request.GET.get('code')
        
        token_req = requests.post(f"https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={redirect_uri}")
        token_req_json = token_req.json()
        # error = token_req_json.get("error")

        # if error is not None:
        #     raise JSONDecodeError(error)
        
        access_token = token_req_json.get('access_token')

        user_data_req = requests.get("https://www.googleapis.com/oauth2/v1/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        user_data_json = user_data_req.json()
        email = user_data_json.get('email')

        try:
            user = User.objects.get(email=email)
            refresh = RefreshToken.for_user(user)
            refresh["email"] = user.email
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK
            )

        except:
            user = User.objects.create_user(email=email)
            user.set_unusable_password()
            user.save()
            refresh = RefreshToken.for_user(user)
            refresh["email"] = user.email
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK
            )

