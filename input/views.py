from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import Input
from prompt.models import Prompt

from .serializers import InputSerializer

# Create your views here.
class InputListView(APIView):
    def post(self, request):
        name = request.data.get('name')
        type = request.data.get('type')
        # content = request.data.get('content')
        prompt = request.data.get('prompt')
        placeholding = request.data.get('placeholding')

        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)
        
        if not Prompt.objects.filter(id=prompt).exists():
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        targetPrompt = Prompt.objects.filter(id=prompt).first()
        
        input = Input.objects.create(name=name, type=type, prompt=targetPrompt, placeholding=placeholding)
        serializer = InputSerializer(input)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class InputDetailView(APIView):
    def delete(self, request, input_id):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication denied"}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            input = Input.objects.get(id=input_id)
        except:
            return Response({"detail": "Input Not found."}, status=status.HTTP_404_NOT_FOUND)
        prompt_id = input.prompt.id
        prompt = Prompt.objects.filter(id=prompt_id).first()
        if request.user != prompt.author:
            return Response({"detail": "You are not an author of this prompt."}, status=status.HTTP_401_UNAUTHORIZED)

        
        input.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    