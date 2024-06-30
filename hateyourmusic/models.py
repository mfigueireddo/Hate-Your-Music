from django.db import models
from django.contrib.auth.models import User

class Music(models.Model):
  name = models.TextField(blank=False)
  artist = models.TextField(blank=False)
  url = models.URLField(blank=False)
  user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)

class Playlist(models.Model):
  name = models.TextField(blank=False)
  cover = models.ImageField(null=True, blank=True, upload_to="playlist_covers/")
  user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
  musics = models.ManyToManyField(Music)

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
  playlists = models.ManyToManyField(Playlist)

class Follow(models.Model):
  user = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
  follower = models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE)
  class Meta:
    unique_together = ('user','follower')