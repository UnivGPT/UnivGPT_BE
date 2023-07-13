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
        pass
    
    def get(self, request):
        prompt_id = request.GET.get('prompt')
        if not prompt_id:
            return Response({"detail": "missing fileds ['prompt']"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not Prompt.objects.filter(id=prompt_id).exists():
            return Response({"detail": "No prompts found."}, status=status.HTTP_404_NOT_FOUND)
        
        inputs = Input.objects.filter(prompt_id=prompt_id)
        serializer = InputSerializer(inputs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class InputDetailView(APIView):
    def delete(self, request, prompt_id):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication denied"}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            input = Input.objects.get(id=prompt_id)
        except:
            return Response({"detail": "Input Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        input.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
