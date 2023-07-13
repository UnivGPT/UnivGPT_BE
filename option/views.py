from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Option
from input.models import Input
from .serializers import OptionSerializer

# Create your views here.

class OptionListView(APIView):
    def get(self, request):
        input_id = request.GET.get('input')
        if not input_id:
            return Response({"detail": "missing fields ['prompt']"}, status=status.HTTP_400_BAD_REQUEST)
        if not Input.objects.filter(id=input_id).exists():
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        options = Option.objects.filter(input=input_id)
        serializer = OptionSerializer(options, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        name = request.data.get('name')
        input_id = request.GET.get('input')
        if not request.user.is_authenticated:
          return Response({"detail": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)
        
        if not name:
            return Response({"detail": "missing fields ['name']"}, status=status.HTTP_400_BAD_REQUEST)
        
        option = Option.objects.create(name=name, input=input_id)
        serializer = OptionSerializer(option)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class OptionDetailView(APIView):
    def delete(self, request, option_id):
        if not request.user.is_authenticated:
          return Response({"detail": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            option = Option.objects.get(id=option_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        option.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    
# class OptionDetailView(APIView):

# def patch(self, request):
#         user = request.user
#         user_serializer = UserSerializer(user, data=request.data, partial=True)
#         if not user_serializer.is_valid(raise_exception=True):
#             return Response({"detail": "user data validation error"}, status=status.HTTP_400_BAD_REQUEST)
#         user_serializer.save()
#         return Response(user_serializer.data, status=status.HTTP_200_OK)