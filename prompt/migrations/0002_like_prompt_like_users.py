# Generated by Django 4.2.3 on 2023-07-12 08:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('prompt', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prompt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prompt.prompt')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='prompt',
            name='like_users',
            field=models.ManyToManyField(blank=True, related_name='liked_prompts', through='prompt.Like', to=settings.AUTH_USER_MODEL),
        ),
    ]