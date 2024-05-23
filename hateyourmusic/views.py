from django.shortcuts import render, redirect
from .models import Profile
from django.contrib.auth.models import User
from django.core.validators import validate_email, URLValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password


def home(request):
  return render(request, "home.html")

def create_user(request):
  if request.method == "POST":

    username = request.POST["username"]

    if User.objects.filter(username=username).first():
      return render(request, "register.html", context={"username_error":True})

    email = request.POST["email"]

    try:
      validate_email(email)
    except ValidationError:
      return render(request, "register.html", context={"invalid_email": True})
    
    if User.objects.filter(email=email).first():
      return render(request, "register.html", context={"email_error":True})

    password = request.POST["password"]
    
    try:
      validate_password(password)
    except Exception as error_message:
      return render(request, "register.html", context={"password_error": True, "error_message": error_message})
      
    user = User.objects.create_user(
      username,
      email,
      password
    )

    user.save()

    url = request.POST["url"]
    
    if url:
      url_validator =  URLValidator()
      try:
        url_validator(url)
      except ValidationError:
        return render(request, "register.html", context={"invalid_url": True})

    name = request.POST["name"]

    if not name:
      name = username
    
    Profile.objects.create(
      user=user,
      biography = request.POST["biography"],
      name = name,
      location = request.POST["location"],
      url = url,
      birthday = request.POST["birthday"] if request.POST["birthday"] else None,
      profile_picture = request.POST["profile_picture"],
      profile_background = request.POST["profile_background"]
    )

    return redirect("home")
  
  return render(request,"register.html")