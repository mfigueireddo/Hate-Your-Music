from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Post(models.Model):
  author = models.CharField(max_length=50, blank=True)
  theme = models.CharField(max_length=100, blank=True)
  content = models.TextField()
  date = models.DateTimeField(auto_now_add=True, blank=True)
  numOfLikes = models.IntegerField(blank=True, null=True,default=0)
  numOfDislikes = models.IntegerField(blank=True, null=True, default=0)
  numOfComments = models.IntegerField(blank=True, null=True, default=0)

class Comment(models.Model):
  post = models.ForeignKey(Post, on_delete=models.CASCADE) # key comment -> post
  author = models.CharField(max_length=50, blank=True)
  content = models.TextField()
  key = models.IntegerField(blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
  comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
  class Meta:
      unique_together = ('user', 'post', 'comment')  # Ensure a user can only like a post/comment once
  def __str__(self):
      if self.post:
          return f"{self.user} liked post {self.post}"
      elif self.comment:
          return f"{self.user} liked comment {self.comment}"
      else:
          return f"{self.user} liked an unknown item"

class Community(models.Model):
  name = models.CharField(max_length=100)
  numOfFans = models.IntegerField()
  description = models.TextField()
  TIPO_DE_COM = {
    ("Ar","Artista"),
    ("Mus","Música"),
    ("Gen","Gênero"),
    ("Al","Álbum"),
}
  coms = models.CharField(max_length=5,choices=TIPO_DE_COM)


class Music(models.Model):
  title = models.CharField(max_length=100)
  artist = models.CharField(max_length=100)
  album = models.CharField(max_length=100)
  genre = models.CharField(max_length=100)
  year = models.IntegerField()
  duration = models.IntegerField()
