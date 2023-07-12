from django.db import models

from django.utils import timezone

# Create your models here.
class Prompt(models.Model):
    title = models.CharField(max_length=32)
    description = models.CharField(max_length=64)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title