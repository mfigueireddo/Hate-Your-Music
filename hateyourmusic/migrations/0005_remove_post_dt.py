# Generated by Django 5.0.2 on 2024-06-03 12:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hateyourmusic', '0004_alter_community_coms'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='dt',
        ),
    ]