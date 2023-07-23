from django.db import models

from prompt.models import Prompt

# Create your models here.
class Input(models.Model):
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE)
    name = models.CharField(max_length=16)
    type = models.IntegerField(default=1)
    placeholding = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name
