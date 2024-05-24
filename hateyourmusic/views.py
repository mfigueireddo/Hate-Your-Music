from django.shortcuts import render, redirect
from .models import Profile
from django.contrib.auth.models import User
from .validate import validador_usuario, validador_email, validador_senha, validador_url, validador_nome, validador_aniversario


def home(request):
  return render(request, "home.html")

def create_user(request):
  
  if request.method == "POST":

    username = request.POST["username"]
    validador_usuario(username,request)

    email = request.POST["email"]
    validador_email(email,request)

    password = request.POST["password"]
    validador_senha(password,request)
      
    user = User.objects.create_user(
      username,
      email,
      password
    )

    user.save()

    url = request.POST["url"]
    validador_url(url,request)

    name = request.POST["name"]
    name = validador_nome(name,username)

    birthday = request.POST["birthday"]
    birthday = validador_aniversario(birthday)
    
    Profile.objects.create(
      user = user,
      biography = request.POST["biography"],
      name = name,
      location = request.POST["location"],
      url = url,
      birthday = birthday,
      profile_picture = request.POST["profile_picture"],
      profile_background = request.POST["profile_background"]
    )

    return redirect("home")
  
  return render(request,"register.html")