from django.shortcuts import render

from .models import Prompt
from .serializers import PromptSerializer

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
# Create your views here.

class PromptDetailView(APIView):
    def get(self, request, prompt_id):
        try:
            prompt = Prompt.objects.get(id=prompt_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = PromptSerializer(prompt)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def delete(self, request, prompt_id):
        try:
            prompt = Prompt.objects.get(id=prompt_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        prompt.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def put(self, request, prompt_id):
        try:
            prompt = Prompt.objects.get(id = prompt_id)
        except:
            if not prompt.request.title or prompt.request.description:
                return Response({"detail": "[title, description] fields missing."})
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        prompt.title = request.data.get('title') or prompt.title
        prompt.description = request.data.get('description') or prompt.description
        prompt.content = request.data.get('content') or prompt.content
        prompt.save()
        return Response("{prompt.title}으로 수정되었음.", status=status.HTTP_200_OK)



