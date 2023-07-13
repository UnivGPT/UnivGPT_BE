from rest_framework.serializers import ModelSerializer
from .models import Prompt
from category.serializers import CategorySerializer
from account.serializers import UserIdUsernameSerializer

class PromptSerializer(ModelSerializer):
    author = UserIdUsernameSerializer(read_only=True)
    category = CategorySerializer(many=True, read_only=True)
    class Meta:
        model = Prompt
        fields = "__all__"