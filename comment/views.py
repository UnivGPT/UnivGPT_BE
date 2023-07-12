from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Comment
from prompt.models import Prompt
from .serializers import CommentSerializer

class CommentListView(APIView):
    def get(self, request):
        prompt_id = request.GET.get('prompt')
        if not prompt_id:
            return Response({"detail": "missing fields ['prompt']"}, status=status.HTTP_400_BAD_REQUEST)
        if not Prompt.objects.filter(id=prompt_id).exists():
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        comments = Comment.objects.filter(post_id=prompt_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        author = request.user
        prompt_id = request.data.get('prompt')
        content = request.data.get('content')
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)
        if not prompt_id or not content:
            return Response({"detail": "missing fields ['prompt', 'content']"}, status=status.HTTP_400_BAD_REQUEST)
        if not Prompt.objects.filter(id=prompt_id).exists():
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        comment = Comment.objects.create(post_id=prompt_id, author=author, content=content)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class CommentDetailView(APIView):
    def delete(self, request, comment_id):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            comment = Comment.objects.get(id=comment_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        if request.user != comment.author:
            return Response({"detail": "Permission denied"}, status=status.HTTP_401_UNAUTHORIZED)

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

