from django.db.models.fields import DateTimeField
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from .models import Community, Music, Post, Comment, Like
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def home(request):
    version = "5" # mudar quando a CARALJHA ALaDA do CSS parar de funcionar
    musics = Music.objects.all()
    communities = Community.objects.all()
    posts = Post.objects.all()
    comments = Comment.objects.all()
    likes = Like.objects.filter(user=request.user, post__in=posts)
    like = Like.objects.all()
    return render(request, "posts.html", context={"music": musics, "community": communities, "post": posts, "comments": comments, "like": like, "version": version, "likes": likes})

def create_post(request):
  if request.method == "POST":
      Post.objects.create(
          author = request.user.username,
          theme = request.POST["theme"],
          content = request.POST["content"]
      )
      return redirect("home")
  return render(request, "forms.html", context={"type": "Criar"})

def update_post(request, id):
  post = Post.objects.get(id = id)
  if request.method == "POST":
      post.author = request.POST["author"]
      post.theme = request.POST["theme"]
      post.content = request.POST["content"]
      post.save()

      return redirect("home")
  return render(request, "forms.html", context={"type": "Atualizar","post": post})

def delete_post(request, id):
  post = Post.objects.get(id = id)
  if request.method == "POST":
      if "confirm" in request.POST:
          post.delete()

      return redirect("home")
  return render(request, "r_u_sure.html", context={"post": post})

def like_post(request, post_id):
  if request.method == "POST":
      post = Post.objects.get(id=post_id)
      user = request.user
      like = Like.objects.create(user=user, post=post)  # Create a like for the post
      post.numOfLikes += 1
      post.save()
      return redirect("home")
  return redirect("home")

def dislike_post(request, post_id):
  if request.method == "POST":
      post = Post.objects.get(id=post_id)
      post.numOfDislikes += 1
      post.save()
      return redirect("home")
  return redirect("home")


@login_required
def create_comment(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_id)
        comment = Comment.objects.create(
            author=request.user.username,
            content=request.POST["content"],
            created_at=timezone.now(),
            post=post
        )
        comment.save()
    return redirect("home")
    
def update_comment(request, comment_id):
  comment = Comment.objects.get(id = comment_id)
  if request.method == "POST":
      comment.content = request.POST["content"]
      comment.save()
      return redirect("home")
  return render(request, "forms_comms.html", context={"type": "Atualizar","comment": comment})

def delete_comment(request, comment_id):
    comment = Comment.objects.get(id = comment_id)
    if request.method == "POST":
        if "confirm" in request.POST:
            comment.delete()
            messages.success(request, 'Comment deleted successfully!') 
            return redirect('home')
    return render(request, "r_u_sure.html", context={"comment": comment})

def create_user(request):
    if request.method == "POST":
        user = User.objects.create_user(request.POST["username"],request.POST["email"],request.POST["password"])
        user.save()
        return redirect("home")
    return render(request, "register.html", context={"action": "Adicionar"})

def login_user(request):
    if request.method == "POST":
        user = authenticate(
            username=request.POST["username"],
            password=request.POST["password"]
        )
        if user is not None:
            login(request, user)
        else:
            return render(request, "login.html", context={"error": "Usuário ou senha inválidos"})

        if request.user.is_authenticated:
            return redirect("home")

        return render(request, "login.html", context={"error_msg": "Usuário não pode ser logado"})
    return render(request, "login.html")

def logout_user(request):
    logout(request)
    return redirect("home")