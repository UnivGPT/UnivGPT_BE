from django.contrib import admin

# Register your models here.
from .models import Prompt, Like

admin.site.register(Prompt)
admin.site.register(Like)