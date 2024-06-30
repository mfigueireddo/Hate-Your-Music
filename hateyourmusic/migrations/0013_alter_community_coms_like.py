# Generated by Django 5.0.2 on 2024-06-12 12:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hateyourmusic', '0012_comment_key_alter_community_coms'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='community',
            name='coms',
            field=models.CharField(choices=[('Gen', 'Gênero'), ('Ar', 'Artista'), ('Mus', 'Música'), ('Al', 'Álbum')], max_length=5),
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hateyourmusic.comment')),
                ('post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hateyourmusic.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'post', 'comment')},
            },
        ),
    ]
