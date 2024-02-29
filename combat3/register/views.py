import django
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout

from django.views import View

# maybe do a helpers.py later
import datetime
from random import randint, choice


username_prefixes = ("fighter", "runner", "quick"
                     , "super", "victorius", "smart"
                     , "kind", "big", "powerful")

# Create your views here.
# later, do a view for localhost:admin/ to return httperror. while the real admin website will be something totally different
# -or not, of course. maybe users, when the website has been published, can't access the admin page.

needed_parameters = ("first_name", "last_name", "username", "password")
def get_which(which):
    return {
        "up": ("POST", "Create an account", "Create Account"),
        "in": ("GET", "Log into your combat account", "Log in"),
     }[which]

def register_page(request, which="up"):
    which = which.lower()
    if which in ("up", "in"):
        if "message" in request.GET:
            message = request.GET["message"]
        else:
            message = ''
        context = {
            "which": get_which(which),
            "message": message,
        }
        return render(request, 'signs.html', context)
    elif which == "out":
        logout(request)
        return redirect("/")
    else:
        raise Http404("Nothing here")

class Log(View):
    def get(self, request):
        response = redirect("/register/sign/in?message=Invalid+username+or+password")

        username = request.GET["username"]
        password = request.GET["password"]
        if password and username:
            # check if user is a combat user
            user = authenticate(request, username=username, password=password)
            if user:
                # login()
                login(request, user)
                response["Location"] = "/lounge"
        return response
        
    
    def post(self, request):
        details = {}
        message = "Account created successfully"
        response = redirect(f"/register/sign/in?message={message}")
        for param in needed_parameters:
            if request.POST[param]:
                details[param] = request.POST[param]
            else:
                message = f"Please enter your {' '.join(param.split('_'))}"
                response["Location"] = f"/register/sign/up?message={message}"
                break
        else:
            # create a user
            try:
                new_user = User.objects.create_user(**details)
                new_user.save()
            except Exception as e:
                if type(e) == django.db.utils.IntegrityError:
                    username = details["username"]
                    new_name = f"{choice(username_prefixes)}{details['first_name'].capitalize()}{randint(11, 500)}"
                    message = f"Username {username} is taken. How about {new_name}?"
                else:
                    message = "An unknown error occured"
                    with open("errors.log", 'a') as file:
                        file.write(f"{datetime.datetime.now()}: {e}")
                response["Location"] = f"/register/sign/up?message={message}"


        return response

def profile_pic(request):
    if request.user.is_authenticated:
        # will be made differently later. Better. everyone with chosen emoji (or picture)
        # with open()
        return render(request, {})