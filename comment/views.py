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
