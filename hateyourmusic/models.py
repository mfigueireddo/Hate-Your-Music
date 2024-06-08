from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
  user = models.OneToOneField(User,null=False, on_delete=models.CASCADE)
  biography = models.TextField(blank=True)
  name = models.TextField(blank=True)
  location = models.TextField(blank=True)
  url = models.URLField(blank=True)
  birthday = models.DateField(null=True, blank=True)
  date_joined = models.DateField(auto_now_add=True)
  icon = models.ImageField(null=True,blank=True,upload_to="profile_icons/")
  background = models.ImageField(null=True,blank=True,upload_to="profile_backgrounds/")