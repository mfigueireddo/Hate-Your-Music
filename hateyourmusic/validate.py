from django.contrib.auth.models import User
from django.core.validators import validate_email, URLValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

def validador_usuario(username,request):
  if User.objects.filter(username=username).first():
    return False
  return True

def validador_email(email,request):
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

def validador_imagem_perfil(image):

  max_width = 800
  max_height = 800
  img = Image.open(image)

  if img.width > max_width or img.height > max_height:
    output_size = (max_width, max_height)
    img.thumbnail(output_size, Image.ANTIALIAS)

    image_io = BytesIO()
    image_format = image.name.split('.')[-1].upper()
    img.save(image_io, format=image_format)

    image = ContentFile(image_io.getvalue(), name=image.name)

  return image

def validador_imagem_fundo(image):
  max_width = 1600
  max_height = 1600
  img = Image.open(image)

  if img.width > max_width or img.height > max_height:
    output_size = (max_width, max_height)
    img.thumbnail(output_size, Image.ANTIALIAS)

    image_io = BytesIO()
    image_format = image.name.split('.')[-1].upper()
    img.save(image_io, format=image_format)

    image = ContentFile(image_io.getvalue(), name=image.name)

  return image