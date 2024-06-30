# Generated by Django 5.0.2 on 2024-06-05 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hateyourmusic', '0011_alter_community_coms'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='key',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='community',
            name='coms',
            field=models.CharField(choices=[('Ar', 'Artista'), ('Al', 'Álbum'), ('Mus', 'Música'), ('Gen', 'Gênero')], max_length=5),
        ),
    ]
