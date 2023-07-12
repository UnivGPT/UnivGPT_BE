from rest_framework.serializers import ModelSerializer
from .models import Prompt

class PromptSerializer(ModelSerializer):
    class Meta:
        model = Prompt
        fields = "__all__"