from django.contrib.auth.models import User
from django.core.validators import validate_email, URLValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from PIL import Image
from io import BytesIO
import os
from django.conf import settings

def validador_usuario(username):
  if User.objects.filter(username=username).first():
    return False
  return True

def validador_email(email):
  try:
    validate_email(email)
  # Email inválido
  except ValidationError:
    return 1
  # Email já consta no banco de dados 
  if User.objects.filter(email=email).first():
    return 2
  return 0

def validador_senha(password,request):
  try:
    validate_password(password,request)
  except Exception as error_message:
    return error_message
  return 0

def validador_url(url):
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

def validador_imagem_perfil(image):

  max_width = 500
  max_height = 500
  aux = Image.open(image)
  
  if aux.width > max_width or aux.height > max_height:
    output_size = (max_width, max_height)
    aux.thumbnail(output_size, Image.Resampling.LANCZOS)
  
    image_io = BytesIO()
    image_format = image.name.split('.')[-1].upper()
    image_format = "JPEG" if image_format == "JPG" else None
    aux.save(image_io, format=image_format)
  
    image_path = os.path.join(settings.MEDIA_ROOT, 'profile_icons', image.name)
    with open(image_path, 'wb') as f:
        f.write(image_io.getvalue())
    image_path = os.path.join('profile_icons', image.name)
    return image_path
  
  return image.path

def validador_imagem_fundo(image):

  max_width = 1600
  max_height = 1600
  aux = Image.open(image)
  
  if aux.width > max_width or aux.height > max_height:
    output_size = (max_width, max_height)
    aux.thumbnail(output_size, Image.Resampling.LANCZOS)
  
    image_io = BytesIO()
    image_format = image.name.split('.')[-1].upper()
    image_format = "JPEG" if image_format == "JPG" else None
    aux.save(image_io, format=image_format)
    
    image_path = os.path.join(settings.MEDIA_ROOT, 'profile_backgrounds', image.name)
    with open(image_path, 'wb') as f:
      f.write(image_io.getvalue())
    image_path = os.path.join('profile_backgrounds', image.name)
    return image_path

  return image.path