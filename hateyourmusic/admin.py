from django.contrib import admin
from .models import Like, Music, Post, Community, Comment

# Register your models here.
admin.site.register(Post)
admin.site.register(Community)
admin.site.register(Music)
admin.site.register(Comment)
admin.site.register(Like)