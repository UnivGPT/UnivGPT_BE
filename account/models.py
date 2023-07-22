from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    socials_id = models.CharField(max_length=128, default="a")
    socials_username = models.CharField(max_length=128, default="")
