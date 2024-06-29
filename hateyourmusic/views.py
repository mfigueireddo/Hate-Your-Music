from django.shortcuts import render, redirect
from .models import Profile, Music, Playlist
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from hateyourmusic import validate
from django.db import transaction
from django.conf import settings
import os

# Geral

def home(request):
  return render(request, "home.html")

def admin_view(request):
  users = User.objects.all()
  profiles = Profile.objects.all()
  musics = Music.objects.all()
  playlists = Playlist.objects.all()
  return render(request,"admin_view.html",context={"users":users,"profiles": profiles,"musics":musics,"playlists":playlists})

# Usuário

def user_create(request):

  if request.method == "POST":

    username = request.POST["username"]
    email = request.POST["email"]
    password = request.POST["password"]
    biography = request.POST["biography"]
    name = request.POST["name"]
    location = request.POST["location"]
    url = request.POST["url"]
    birthday = request.POST["birthday"]
    icon = request.FILES.get("icon")
    background = request.FILES.get("background")
    
    if not validate.validador_usuario(username): 
      return render(request, "user_create.html", context={"username_error":True})

    # Caso o email seja inválido
    if validate.validador_email(email) == 1:
      return render(request, "user_create.html", context={"invalid_email": True})
    # Caso o email já esteja cadastrado no sistema
    elif validate.validador_email(email) == 2:
      return render(request, "user_create.html", context={"email_error":True})

    password_error_message = validate.validador_senha(password,request)
    if password_error_message != 0:
      return render(request, "user_create.html", context={"password_error": True, "password_error_message": password_error_message})

    if not validate.validador_url(url):
      render(request, "user_create.html", context={"invalid_url": True})

    name = validate.validador_nome(name,username)
    
    birthday = validate.validador_aniversario(birthday)

    if icon:
      icon.name = str(id) + '.' + icon.name.split('.')[-1]
      icon_path = validate.validador_icon(icon)
    else:
      icon_path = settings.DEFAULT_ICON_IMAGE_PATH
    
    if background:
      background.name = str(id) + '.' + background.name.split('.')[-1]
      background_path = validate.validador_fundo(background)
    else:
      background_path = settings.DEFAULT_BACKGROUND_IMAGE_PATH
      
    # Garante que o usuário seja criado juntamente ao perfil
    try:
      
      with transaction.atomic():
          user = User.objects.create_user(
              username=username,
              email=email,
              password=password
          )
          Profile.objects.create(
              user=user,
              biography=biography,
              name=name,
              location=location,
              url=url,
              birthday=birthday,
              icon=icon_path,
              background=background_path,
          )
        
      return redirect("home")
      
    except Exception as erro:
      return render(request, "user_create.html", context={"creation_error":True,"creation_error_message": str(erro)})

  return render(request,"user_create.html")

def user_login(request):

  if request.method == "POST":

    username = request.POST["username"]
    password = request.POST["password"]

    user = authenticate(username=username,password=password)

    if user:
      login(request, user)
      return redirect("home")

    else:
      return render(request, "user_login.html", context={"error_message": "Credenciais inválidas. Por favor, tente novamnete"})

  return render(request, "user_login.html")

def user_logout(request):
  logout(request)
  return redirect("home")

def user_delete(request,id):

  user = User.objects.get(id=id)
  profile = Profile.objects.get(user=user)

  if request.method=="POST":

    if "sim" in request.POST:
      if profile.icon.name != "default/default_icon.jpg":
        caminho = os.path.join(settings.MEDIA_ROOT,profile.icon.name)
        os.remove(caminho)
      if profile.background.name != "default/default_background.jpg":
        caminho = os.path.join(settings.MEDIA_ROOT,profile.background.name)
        os.remove(caminho)
      user.delete()
    
    return redirect("home")

  return render(request, "user_delete_confirmation.html", context={"user":user})

def user_update(request,id):

  user = User.objects.get(id = id)
  profile = Profile.objects.get(user=user)
  
  if request.method == "POST":

    username = request.POST["username"]
    email = request.POST["email"]
    biography = request.POST["biography"]
    name = request.POST["name"]
    location = request.POST["location"]
    url = request.POST["url"]
    birthday = request.POST["birthday"]
    icon = request.FILES.get("icon")
    background = request.FILES.get("background")

    if username != user.username:
      if not validate.validador_usuario(username):
          return render(request, "user_update.html", context={"username_error":True,"profile":profile,"user":user})
      else:
        user.username = username

    if email != user.email:
      # Caso o email seja inválido
      if validate.validador_email(email) == 1:
        return render(request, "user_update.html", context={"invalid_email": True,"profile":profile,"user":user})
      # Caso o email já esteja cadastrado no sistema
      elif validate.validador_email(email) == 2:
        return render(request, "user_update.html", context={"email_error":True,"profile":profile,"user":user})
      else:
        user.email = email

    if biography:
      if biography != profile.biography:
        profile.biography = biography

    if name:
      if name != profile.name:
        profile.name = name

    if location:
      if location != profile.location:
        profile.location = location
    
    if url:
      if url != profile.url:
        if not validate.validador_url(url):
          render(request, "user_update.html", context={"invalid_url": True,"profile":profile,"user":user})
        else:
          user.url = url

    if birthday != profile.birthday:
      profile.birthday = validate.validador_aniversario(birthday)

    if icon:
      if profile.icon.name != "default/default_icon.jpg":
        caminho = os.path.join(settings.MEDIA_ROOT,profile.icon.name)
        os.remove(caminho)
      icon.name = str(id) + '.' + icon.name.split('.')[-1]
      profile.icon = validate.validador_icon(icon)

    if background:
      if profile.background.name != "default/default_background.jpg":
        caminho = os.path.join(settings.MEDIA_ROOT,profile.background.name)
        os.remove(caminho)
      background.name = str(id) + '.' + background.name.split('.')[-1]
      profile.background = validate.validador_fundo(background)
    
    user.save()
    profile.save()
  
    return redirect("home")
  
  return render(request, "user_update.html", context={"profile":profile,"user":user})

def user_view(request,id):
  user = User.objects.get(id = id)
  profile = Profile.objects.get(user=user)
  return render(request,"user_view.html",context={"profile":profile,"user":user})

# Senha

def password_update(request,id):
  
  if request.method=="POST":

    user = User.objects.get(id = id)

    password = request.POST["password"]
    new_password_1 = request.POST["new_password_1"]
    new_password_2 = request.POST["new_password_2"]

    if not user.check_password(password):
      return render(request,"password_update.html", context={"password_error":True})

    elif new_password_1 != new_password_2:
      return render(request,"password_update.html", context={"new_password_cmp_error":True})

    else:
      error_message = validate.validador_senha(new_password_1,request)
      if error_message != 0:
        return render(request, "password_update.html", context={"new_password_error": True, "error_message": error_message})

      user.set_password(new_password_1)
      user.save()
      
    return redirect("home")

  return render(request,"password_update.html")

# Música

def music_create(request):

  if request.method=="POST":
    
    name = request.POST["name"]
    artist = request.POST["artist"]
    url = request.POST["url"]

    if not validate.validador_url(url):
      return render(request, "music_register.html", context={"invalid_url": True})
    
    Music.objects.create(
      name = name,
      artist = artist,
      url = url
    )
    return redirect("home")
  
  return render(request, "music_create.html")

def music_delete(request,id):

  music = Music.objects.get(id=id)

  if request.method=="POST":

    if "sim" in request.POST:
      music.delete()

    return redirect("home")

  return render(request, "music_delete_confirmation.html", context={"music":music})

def music_update(request,id):

  music = Music.objects.get(id=id)

  if request.method=="POST":
    name = request.POST["name"]
    artist = request.POST["artist"]
    url = request.POST["url"]

    if name != music.name:
      music.name = name

    if artist != music.artist:
      music.artist = artist

    if url != music.url:
      if not validate.validador_url(url):
        return render(request, "music_update.html", context={"invalid_url": True})
      else:
        music.url = url

    return redirect("home")
      
  return render(request, "music_update.html")

def music_view(request, id):
  music = Music.objects.get(id=id)
  return render(request, "music_view.html",context={"music":music})

# Playlist

def playlist_create(request, id):
  if request.method == "POST":
    user = User.objects.get(id = id)

    name = request.POST["name"]
    cover = request.POST["cover"]

    if cover:
      cover.name = str(id) + '.' + cover.name.split('.')[-1]
      cover_path = validate.validador_cover(cover)
    else:
      cover_path = settings.DEFAULT_COVER_IMAGE_PATH

    Playlist.objects.create(
      name = name,
      cover = cover_path,
      user = user
    )
    return redirect("home")
  
  return render(request,"playlist_create.html")

def playlist_add_music(request,id):

  playlist = Playlist.objects.get(id=id)
  musics = Music.objects.all()

  if request.method == "POST":
    music = request.POST["music"]
    playlist.musics.add(music)

  return render(request,"playlist_add_music.html", context={"playlist":playlist,"musics":musics})

def playlist_delete(request,id):

  playlist = Playlist.objects.get(id=id)

  if request.method == "POST":
    if "sim" in request.POST:
      playlist.delete()
    return redirect("home")
  
  return render(request, "playlist_delete_confirmation.html")

def playlist_view(request,id):

  playlist = Playlist.objects.get(id=id)
  
  return render(request,"playlist_view.html",context={"playlist":playlist})