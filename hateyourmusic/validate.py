from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.validators import validate_email, URLValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

def validador_usuario(username,request):
  if User.objects.filter(username=username).first():
    return False
  return True

def validador_email(email,request):
  try:
    validate_email(email)
  except ValidationError:
    return 1
  if User.objects.filter(email=email).first():
    return 2
  return 0

def validador_senha(password,request):
  try:
    validate_password(password,request)
  except Exception as error_message:
    return error_message
  return 0

def validador_url(url,request):
  if url:
    url_validator =  URLValidator()
    try:
      url_validator(url)
    except ValidationError:
      return False
  return True

def validador_nome(name,username):
  if not name:
    name = username
  return name

def validador_aniversario(birthday):
  if birthday:
    return birthday
  else:
    return None