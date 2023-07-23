from django.db import models

from input.models import Input

# Create your models here.
class Option(models.Model):
    name = models.CharField(max_length=16)
    input = models.ForeignKey(Input, on_delete=models.CASCADE)

    def __str__(self):
        return self.name