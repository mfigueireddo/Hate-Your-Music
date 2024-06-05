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
  picture = models.ImageField(default="profile_default.jpg", upload_to="profile_pictures/")
  background = models.ImageField(default="background_default.png", upload_to="profile_backgrounds/")