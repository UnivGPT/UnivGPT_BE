# Generated by Django 4.2.3 on 2023-07-22 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_remove_userprofile_socials_userprofile_socials_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='socials_username',
            field=models.CharField(default='', max_length=128),
        ),
    ]
