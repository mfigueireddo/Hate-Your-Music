# Generated by Django 5.0.2 on 2024-05-23 14:27

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hateyourmusic', '0002_profile_birthday_profile_date_joined_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_background',
            field=models.ImageField(blank=True, storage=django.core.files.storage.FileSystemStorage('/media/profile_background'), upload_to=''),
        ),
        migrations.AddField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(blank=True, storage=django.core.files.storage.FileSystemStorage('/media/profile_pictures'), upload_to=''),
        ),
    ]