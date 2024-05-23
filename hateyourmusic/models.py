from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.utils import timezone

fs_picture = FileSystemStorage("/media/profile_pictures")
fs_background = FileSystemStorage("/media/profile_background")

class Profile(models.Model):
  user = models.OneToOneField(User,null=True, on_delete=models.CASCADE)
  biography = models.TextField(blank=True)
  name = models.TextField(blank=True)
  location = models.TextField(blank=True)
  url = models.URLField(blank=True)
  birthday = models.DateField(default = timezone.now, blank=True)
  date_joined = models.DateField(default = timezone.now, blank=True)
  profile_picture = models.ImageField(storage = fs_picture, blank=True)
  profile_background = models.ImageField(storage = fs_background, blank=True)