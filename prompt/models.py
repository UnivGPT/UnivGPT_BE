from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from category.models import Category
from input.models import Input

# Create your models here.
class Prompt(models.Model):
    title = models.CharField(max_length=32)
    description = models.CharField(max_length=64)
    content = models.TextField()
    view = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    like_users = models.ManyToManyField(User, blank=True, related_name='liked_prompts', through='Like')
    author = models.ForeignKey(User, related_name='like_prompt', through='Like')
    category = models.ManyToManyField(Category, blank=True, related_name='prompts')
    

    def __str__(self):
        return self.title
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE)
