from rest_framework.serializers import ModelSerializer, SerializerMethodField
from django.contrib.auth.models import User
from rest_framework.serializers import ValidationError
from .models import UserProfile

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "password", "is_superuser", "username"]

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        password = attrs.get('password', '')
        if not (email and username and password):
            raise ValidationError({"detail": "[email, username, password] fields missing."})
        return attrs
    
class UserProfileSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = "__all__"

class UserIdUsernameSerializer(ModelSerializer):
    socials_username = SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "socials_username"]

    def get_socials_username(self, obj):
        try:
            return obj.userprofile.socials_username
        except UserProfile.DoesNotExist:
            return None

class SecureUserSerializer(ModelSerializer):
    profile = UserProfileSerializer(source='userprofile', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'profile']

    def get_fields(self):
        fields = super().get_fields()
        fields['profile'].fields.pop('user')
        fields['profile'].fields.pop('socials_id')
        return fields