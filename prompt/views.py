from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.views import status
from .models import Prompt, Like
from .serializers import PromptSerializer

# Create your views here.
class LikeView(APIView):
    def post(self, request, prompt_id):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            prompt = Prompt.objects.get(id=prompt_id)
        except:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        
        like_list = prompt.like_set.filter(user=request.user)
        if like_list.count() > 0:
            prompt.like_set.get(user=request.user).delete()
        else:
            Like.objects.create(user=request.user, prompt=prompt)
        
        serializer = PromptSerializer(instance=prompt)
        return Response(serializer.data, status=status.HTTP_200_OK)
        