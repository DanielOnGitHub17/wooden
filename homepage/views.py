from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from datetime import datetime
from helpers import show_message

# Create your views here.

def home(request):
    return render(request, "base.html", {"user": request.user})

def leaders(request):
    return render(request, "leaders.html", {"user": request.user})

def game_help(request):
    return render(request, "game_help.html", {"user": request.user})

class Support(View):
    def post(self, request):
        with open("../issues.html", 'a') as file:
            file.write(f"\n<li>{request.user}: {request.POST['issue']} | {datetime.now()}</li>")
        request.session["message"] = "Thanks for sending a message!"
        return redirect("/support/")
    
    def get(self, request):
        context = {
            "message": show_message(request),
        }
        return render(request, "support.html", context)

def dev(request):
    return render(request, "dev.html", {"user": request.user})
