from django.shortcuts import render

# Create your views here.
from prompt.models import Prompt
from prompt.serializers import PromptSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category
from .serializers import CategorySerializer

class CategoryListView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(instance=categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)
        if not request.user.is_superuser:
            return Response({"detail": "not a superuser"}, status=status.HTTP_401_UNAUTHORIZED)
        name = request.data.get('name')
        if not name:
            return Response({"detail": "missing fields ['name']"}, status=status.HTTP_400_BAD_REQUEST)
        if Category.objects.filter(name=name).exists():
            return Response({"detail" : "Category with same name already exists"}, status=status.HTTP_409_CONFLICT)
        category = Category.objects.create(name=name)
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CategoryDetailView(APIView):
    def get(self, request, category_id):
        try:
            category = Category.objects.get(id=category_id)
        except:
            return Response({"detail": "Provided category does not exist."}, status=status.HTTP_404_NOT_FOUND)
        prompts = Prompt.objects.filter(category=category)
        serializer = PromptSerializer(instance=prompts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



