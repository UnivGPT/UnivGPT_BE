from django.shortcuts import render
from .models import User
from .serializers import UserSerializer

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

def generate_token_in_serialized_data(user:User) -> UserSerializer.data:
    token = RefreshToken.for_user(user)
    refresh_token, access_token = str(token), str(token.access_token)
    serialized_data = UserSerializer(user).data
    serialized_data['token']={"access":access_token, "refresh":refresh_token}
    return serialized_data

# Create your views here.
class SignupView(APIView):
    def post(self, request):
        user_serializer = UserSerializer(data = request.data)
        if user_serializer.is_valid(raise_exception=True):
            user = user_serializer.save()
        
        serialized_data = generate_token_in_serialized_data(user)
        return Response(serialized_data, status=status.HTTP_201_CREATED)