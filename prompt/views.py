from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import Prompt
from .serializers import PromptSerializer

# Create your views here.
class PromptListView(APIView):
    def get(self, request):
        prompts = Prompt.objects.all()
        serializer = PromptSerializer(prompts, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        title = request.data.get('title')
        description = request.data.get('description')
        content = request.data.get('content')

        if not title or not content or not description:
            return Response({"detail": "fields missing."}, status=status.HTTP_400_BAD_REQUEST)
        
        prompt = Prompt.objects.create(title=title, description=description, content=content, view=0)
        serializer = PromptSerializer(prompt)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    