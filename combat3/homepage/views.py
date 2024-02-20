from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    return render(request, "homepage.html", {"user": request.user})

def leaders(request):
    return render(request, "homepage.html", {"user": request.user})

def game_help(request):
    return render(request, "homepage.html", {"user": request.user})

def support(request):
    return render(request, "homepage.html", {"user": request.user})

def dev(request):
    return render(request, "homepage.html", {"user": request.user})
