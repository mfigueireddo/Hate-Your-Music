# Generated by Django 5.0.2 on 2024-06-03 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hateyourmusic', '0010_alter_comment_post_alter_community_coms'),
    ]

    operations = [
        migrations.AlterField(
            model_name='community',
            name='coms',
            field=models.CharField(choices=[('Gen', 'Gênero'), ('Ar', 'Artista'), ('Mus', 'Música'), ('Al', 'Álbum')], max_length=5),
        ),
    ]