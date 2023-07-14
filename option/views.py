from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Option
from input.models import Input
from prompt.models import Prompt
from .serializers import OptionSerializer

# Create your views here.

class OptionListView(APIView):
    def get(self, request):
        input_id = request.data.get('input')
        if not input_id:
            return Response({"detail": "missing fields ['input']"}, status=status.HTTP_400_BAD_REQUEST)
        if not Input.objects.filter(id=input_id).exists():
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        options = Option.objects.filter(input=input_id)
        serializer = OptionSerializer(options, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        name = request.data.get('name')
        input_id = request.data.get('input')
        if not request.user.is_authenticated:
          return Response({"detail": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)
        
        if not name:
            return Response({"detail": "missing fields ['name']"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = request.user
        
        input = Input.objects.get(id=input_id)

        prompt_id = input.prompt.id
        prompt = Prompt.objects.get(id=prompt_id)
        
        if user != prompt.author:
            return Response({"detail": "not the author of this prompt"}, status=status.HTTP_401_UNAUTHORIZED)
        
        if input.type != 0:
            return Response({"detail": "invalid input type"}, status=status.HTTP_400_BAD_REQUEST)
        
        option = Option.objects.create(name=name, input=input)
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

        user = request.user

        input_id = option.input.id
        input = Input.objects.get(id=input_id)

        prompt_id = input.prompt.id
        prompt = Prompt.objects.get(id=prompt_id)
        
        if user != prompt.author:
            return Response({"detail": "not the author of this prompt"}, status=status.HTTP_401_UNAUTHORIZED)
        
        option.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def patch(self, request, option_id):
        if not request.user.is_authenticated:
          return Response({"detail": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)
        option = Option.objects.get(id=option_id)

        user = request.user

        input_id = option.input.id
        input = Input.objects.get(id=input_id)

        prompt_id = input.prompt.id
        prompt = Prompt.objects.get(id=prompt_id)
        
        if user != prompt.author:
            return Response({"detail": "not the author of this prompt"}, status=status.HTTP_401_UNAUTHORIZED)
        
        if request.data['input'] != input_id:
            return Response({"detail": "input id should not be changed."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = OptionSerializer(option, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response({"detail": "data validation error"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
