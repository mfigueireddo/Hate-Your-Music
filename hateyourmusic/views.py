from django.shortcuts import render

def home(request):
  Version = "2"
  return render(request, "home.html")