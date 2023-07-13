from rest_framework.serializers import ModelSerializer
from .models import Option

class OptionSerializer(ModelSerializer):
    class Meta:
        model = Option
        fields = "__all__"