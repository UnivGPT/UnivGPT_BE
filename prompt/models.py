from django.db import models

from django.utils import timezone

# Create your models here.
class Prompt(models.Model):
    title = models.CharField(max_length=32)
    description = models.CharField(max_length=64)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    #like_users = models.ManyToManyField(User, blank=True, related_name='liked_prompts', through='Like')

    def __str__(self):
        return self.title
    
class Like(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE)