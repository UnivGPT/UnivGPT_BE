from rest_framework.serializers import ModelSerializer

from .models import Input

class InputSerializer(ModelSerializer):
    class Meta:
        model = Input
        fields = "__all__"