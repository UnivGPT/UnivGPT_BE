from django.db import models

# Create your models here.
class Option(models.Model):
    name = models.CharField(max_length=16)