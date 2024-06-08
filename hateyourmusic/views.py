from django.shortcuts import render, redirect
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from hateyourmusic import validate
from django.db import transaction
from django.conf import settings
import os

def home(request):
  return render(request, "home.html")

def create_user(request):

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
      return render(request, "user_register.html", context={"username_error":True})

    # Caso o email seja inválido
    if validate.validador_email(email) == 1:
      return render(request, "user_register.html", context={"invalid_email": True})
    # Caso o email já esteja cadastrado no sistema
    elif validate.validador_email(email) == 2:
      return render(request, "user_register.html", context={"email_error":True})

    password_error_message = validate.validador_senha(password,request)
    if password_error_message != 0:
      return render(request, "user_register.html", context={"password_error": True, "password_error_message": password_error_message})

    if not validate.validador_url(url):
      render(request, "user_register.html", context={"invalid_url": True})

    name = validate.validador_nome(name,username)
    
    birthday = validate.validador_aniversario(birthday)

    if icon:
      icon.name = str(username) + '.' + icon.name.split('.')[-1]
      icon_path = validate.validador_imagem_perfil(icon)
    else:
      icon_path = settings.DEFAULT_ICON_IMAGE_PATH
    
    if background:
      background.name = str(username) + '.' + background.name.split('.')[-1]
      background_path = validate.validador_imagem_fundo(background)
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
      return render(request, "user_register.html", context={"creation_error":True,"creation_error_message": str(erro)})

  return render(request,"user_register.html")

def login_user(request):

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

def logout_user(request):
  logout(request)
  return redirect("home")

def delete_user(request,id):

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

def update_user(request,id):

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

        if profile.icon.name != "default/default_icon.jpg":
          
          caminho_icon_antigo = os.path.join(settings.MEDIA_ROOT,profile.icon.name)
          profile.icon.name = "profile_icons/" + str(username) + '.' + profile.icon.name.split('.')[-1]
          caminho_icon_novo = os.path.join(settings.MEDIA_ROOT,profile.icon.name)
          os.rename(caminho_icon_antigo,caminho_icon_novo)


        if profile.background.name != "default/default_background.jpg":
          
          caminho_background_antigo = os.path.join(settings.MEDIA_ROOT,profile.background.name)
          profile.background.name = "profile_backgrounds/" + str(username) + '.' + profile.background.name.split('.')[-1]
          caminho_background_novo = os.path.join(settings.MEDIA_ROOT,profile.background.name)
          os.rename(caminho_background_antigo,caminho_background_novo)

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
      icon.name = str(username) + '.' + icon.name.split('.')[-1]
      profile.icon = validate.validador_imagem_perfil(icon)

    if background:
      if profile.background.name != "default/default_background.jpg":
        caminho = os.path.join(settings.MEDIA_ROOT,profile.background.name)
        os.remove(caminho)
      background.name = str(username) + '.' + background.name.split('.')[-1]
      profile.background = validate.validador_imagem_fundo(background)
    
    user.save()
    profile.save()
  
    return redirect("home")
  
  return render(request, "user_update.html", context={"profile":profile,"user":user})

def update_password(request,id):
  
  if request.method=="POST":

    user = User.objects.get(id = id)

    password = request.POST["password"]
    new_password_1 = request.POST["new_password_1"]
    new_password_2 = request.POST["new_password_2"]

    if not user.check_password(password):
      return render(request,"user_update_password.html", context={"password_error":True})

    elif new_password_1 != new_password_2:
      return render(request,"user_update_password.html", context={"new_password_cmp_error":True})

    else:
      error_message = validate.validador_senha(new_password_1,request)
      if error_message != 0:
        return render(request, "user_update_password.html", context={"new_password_error": True, "error_message": error_message})

      user.set_password(new_password_1)
      user.save()
      
    return redirect("home")

  return render(request,"user_update_password.html")

def show_profile(request,id):
  user = User.objects.get(id = id)
  profile = Profile.objects.get(user=user)
  return render(request,"user_profile.html",context={"profile":profile,"user":user})

def admin_view(request):
  users = User.objects.all()
  profiles = Profile.objects.all()
  return render(request,"admin_view.html",context={"users":users,"profiles": profiles})