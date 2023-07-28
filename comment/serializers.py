from rest_framework.serializers import ModelSerializer
from .models import Comment
from account.serializers import UserIdUsernameSerializer

class CommentSerializer(ModelSerializer):
    author = UserIdUsernameSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = "__all__"