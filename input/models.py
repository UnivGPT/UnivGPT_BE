from django.db import models
from  django.contrib.postgres.fields import ArrayField

# Create your models here.
class Input(models.Model):
    name = models.CharField(max_length=16)
    type = models.IntegerField(default=1)
    options = ArrayField(models.CharField(max_length=8), blank=True)
    content = models.TextField()

    def __str__(self):
        return self.name