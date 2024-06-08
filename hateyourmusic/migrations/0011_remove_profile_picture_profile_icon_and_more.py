# Generated by Django 5.0.2 on 2024-06-08 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hateyourmusic', '0010_alter_profile_background_alter_profile_picture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='picture',
        ),
        migrations.AddField(
            model_name='profile',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='profile_icons/'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='background',
            field=models.ImageField(blank=True, null=True, upload_to='profile_backgrounds/'),
        ),
    ]