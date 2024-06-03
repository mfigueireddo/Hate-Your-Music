from django.shortcuts import render, redirect
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from hateyourmusic import validate
from django.db import transaction

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
    profile_picture = request.POST["profile_picture"]
    profile_background = request.POST["profile_background"]
    
    if not validate.validador_usuario(username,request): 
      return render(request, "user_register.html", context={"username_error":True})

    # Caso o email seja inválido
    if validate.validador_email(email,request) == 1:
      return render(request, "user_register.html", context={"invalid_email": True})
    # Caso o email já esteja cadastrado no sistema
    elif validate.validador_email(email,request) == 2:
      return render(request, "user_register.html", context={"email_error":True})

    password_error_message = validate.validador_senha(password,request)
    if password_error_message != 0:
      return render(request, "user_register.html", context={"password_error": True, "password_error_message": password_error_message})

    if not validate.validador_url(url,request):
      render(request, "user_register.html", context={"invalid_url": True})

    name = validate.validador_nome(name,username)
    
    birthday = validate.validador_aniversario(birthday)

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
              profile_picture=profile_picture,
              profile_background=profile_background
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

  if request.method=="POST":

    if "sim" in request.POST:
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
    profile_picture = request.POST["profile_picture"]
    profile_background = request.POST["profile_background"]
    
    if username != user.username and validate.validador_usuario(username,request):
        return render(request, "user_update.html", context={"username_error":True})

    # Caso o email seja inválido
    if validate.validador_email(email,request) == 1:
      return render(request, "user_update.html", context={"invalid_email": True})
    # Caso o email já esteja cadastrado no sistema
    elif validate.validador_email(email,request) == 2:
      return render(request, "user_update.html", context={"email_error":True})

    if not validate.validador_url(url,request):
      render(request, "user_update.html", context={"invalid_url": True})

    birthday = validate.validador_aniversario(birthday)

    user.username = username
    user.email = email
    profile.biography = biography
    profile.name = name
    profile.location = location
    profile.url = url
    profile.birthday = birthday
    profile.profile_picture = profile_picture
    profile.profile_background = profile_background
    
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