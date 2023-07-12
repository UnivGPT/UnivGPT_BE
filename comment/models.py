from django.db import models
from django.contrib.auth.models import User
from prompt.models import Prompt
from django.utils import timezone

# Create your models here.
class Comment(models.Model):
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE)
    content = models.CharField(max_length=64)
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
