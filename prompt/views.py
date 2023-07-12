from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.views import status
from .models import Prompt, Like

# Create your views here.
class LikeView(APIView):
    def post(self, request, prompt_id):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            post = Prompt.objects.get(id=prompt_id)
        except:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        