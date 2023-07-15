from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .serializers import PromptSerializer
from .models import Prompt, Like
from .serializers import PromptSerializer
from category.models import Category



# Create your views here.
class PromptListView(APIView):
    def get(self, request):
        prompts = Prompt.objects.all()
        serializer = PromptSerializer(prompts, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        author = request.user
        title = request.data.get('title')
        description = request.data.get('description')
        content = request.data.get('content')
        categories = request.data.get('category')

        print("==================")
        print(categories)

        if not author.is_authenticated:
            return Response({"detail": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)
        
        if not title or not content or not description:
            return Response({"detail": "fields missing."}, status=status.HTTP_400_BAD_REQUEST)
        
        prompt = Prompt.objects.create(title=title, description=description, content=content, view=0, author=author)

        prompt.category.clear()

        for category in categories:
            if Category.objects.filter(name=category).exists():
                prompt.category.add(Category.objects.get(name=category))
        serializer = PromptSerializer(prompt)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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
        if request.user != prompt.author:
            return Response({"detail": "Permission denied"}, status=status.HTTP_401_UNAUTHORIZED)
        prompt.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def put(self, request, prompt_id):
        try:
            prompt = Prompt.objects.get(id = prompt_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        if not request.data['title'] or not request.data['description']:
            return Response({"detail": "[title, description] fields missing."})
        prompt.title = request.data.get('title') or prompt.title
        prompt.description = request.data.get('description') or prompt.description
        prompt.content = request.data.get('content') or prompt.content
        category_names = request.data.get('category')
        if category_names:
            categories = Category.objects.filter(name__in=category_names)
            if len(categories) != len(category_names):
                return Response({"detail": "invalid category"}, status=status.HTTP_400_BAD_REQUEST)
            prompt.category.set(categories)
        prompt.save()
        return Response(f"{prompt.title}으로 수정되었음.", status=status.HTTP_200_OK)

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
        
