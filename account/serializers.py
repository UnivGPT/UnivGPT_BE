from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from rest_framework.serializers import ValidationError

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "password", "is_superuser"]

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        if not (email and password):
            raise ValidationError({"detail": "[email, password] fields missing."})
        return attrs

class UserIdUsernameSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]