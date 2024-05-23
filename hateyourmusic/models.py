from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage

fs_picture = FileSystemStorage("/media/profile_pictures")
fs_background = FileSystemStorage("/media/profile_background")

class Profile(models.Model):
  user = models.OneToOneField(User,null=False, on_delete=models.CASCADE)
  biography = models.TextField(blank=True)
  name = models.TextField(blank=True)
  location = models.TextField(blank=True)
  url = models.URLField(blank=True)
  birthday = models.DateField(null=True, blank=True)
  date_joined = models.DateField(auto_now_add=True)
  profile_picture = models.ImageField(storage = fs_picture, blank=True)
  profile_background = models.ImageField(storage = fs_background, blank=True)