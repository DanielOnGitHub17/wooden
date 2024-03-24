from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime

# Create your views here.

def home(request):
    return render(request, "homepage.html", {"user": request.user})

def leaders(request):
    return render(request, "leaders.html", {"user": request.user})

def game_help(request):
    return render(request, "game_help.html", {"user": request.user})

def support(request, message=''):
    if not message and "issue" in request.POST and len(request.POST["issue"].strip()) > 9:
        with open("issues.html", 'a') as file:
            file.write(f"\n<li>{request.user}: {request.POST['issue']} | {datetime.now()}</li>")
        message = "Thanks for submitting your thoughts. We now have access to your mind."
        return support(request, message)
    return render(request, "support.html", {"user": request.user, "message": message})

def dev(request):
    return render(request, "dev.html", {"user": request.user})
