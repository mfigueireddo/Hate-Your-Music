# Generated by Django 5.0.2 on 2024-06-08 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hateyourmusic', '0014_alter_profile_background_alter_profile_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='background',
            field=models.ImageField(default='default/default_background.jpg', upload_to='profile_backgrounds/'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='icon',
            field=models.ImageField(default='default/default_icon.jpg', upload_to='profile_icons/'),
        ),
    ]
