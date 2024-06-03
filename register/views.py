from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse, HttpRequest
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.views import View
from register.forms import SignInForm, SignUpForm

from game.models import Player
from helpers import show_message, handle_error, WalkError

# maybe do a helpers.py later
import datetime
from random import randint, choice

username_prefixes = ("fighter", "runner", "quick"
                     , "super", "victorious", "smart"
                     , "kind", "big", "powerful"
                     , "brave", "mighty", "potent")

new_username = lambda name: f"{choice(username_prefixes)}{name.capitalize()}{randint(11, 500)}"

# Create your views here.
# later, do a view for localhost:admin/ to return httperror. while the real admin website will be something totally different
# -or not, of course. maybe users, when the website has been published, can't access the admin page.

needed_parameters = ("first_name", "last_name", "username", "password")

class SignUp(View):
    def post(self, request):
        # sign function can still be made useful
        self.POST = request.POST
        result = sign(self.function, self.failed)
        request.session["message"] = result["message"]
        return redirect ("/signin/" if result["success"] else "/signup/")

    def function(self):
        form = SignUpForm(self.POST)
        if not form.is_valid():
            raise WalkError("Invalid form details, make sure all instructions are followed")
        new_user = form.save()
        new_player = Player(user=new_user)
        new_player.save()
        return "Account created successfully"
    
    def failed(self, error):
        if str(error).startswith("UNIQUE constraint failed"):
            username = self.request.POST["username"]
            return f"Username {username} is taken. How about {new_username(self.request.POST["first_name"])}?"        
            
    def get(self, request):
        return register_page(request, "up")

class SignIn(View):
    def post(self, request):
        self.request = request
        self.POST = request.POST
        result = sign(self.function, self.failed)
        request.session["message"] = result["message"]
        return redirect ("/lounge/" if result["success"] else "/signin/")
    
    def function(self):
        user = authenticate(
            self.request,
            username=self.POST["username"],
            password=self.POST["password"]
        )
        player = user.player
        player.logged_in = True
        player.score = 0
        player.save()
        login(self.request, user)
    
    def failed(self, error):
        return "Invalid username or password"

    def get(self, request):
        return register_page(request, "in")

class SignOut(View):
    def post(self, request):
        player = request.user.player
        if player.game:
            return redirect("/lounge/")
        logout(request)
        player.logged_in = False
        player.save()
        return redirect("/")


def sign(function, failed: lambda error: None):
    message = "An unknown error occured"
    success = False
    try:
        message = function()
        success = True
    except WalkError as error:
        message = str(error)
    except Exception as error:
        message = failed(error) or message
        handle_error(error)
    return {"message": message, "success": success}

def get_which(which):
    return {
        "up": ("signup", "Create an account", "Create Account"),
        "in": ("signin", "Log into your wooden account", "Log in"),
     }[which]

def register_page(request, which):
    context = {
        "which": get_which(which),
        "message": show_message(request),
        "form": eval(f"Sign{which.capitalize()}Form"),
    }
    return render(request, "signs.html", context)

def profile_pic(self, request):
    if request.user.is_authenticated:
        # will be made differently later. Better. everyone with chosen emoji (or picture)
        # with open()
        return render(request, {})