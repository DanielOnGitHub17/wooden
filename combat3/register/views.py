from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

from django.views import View

# Create your views here.

needed_parameters = ("first_name", "last_name", "username", "password")
def get_which(which):
    return {
        "up": ("POST", "Create an account", "Create Account"),
        "in": ("GET", "Log into your combat account", "Log in"),
     }[which]

def register_page(request, which="up"):
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
        print(*dir(response), sep='\n')
        for param in needed_parameters:
            if request.POST[param]:
                details[param] = request.POST[param]
            else:
                message = f"Please enter your {' '.join(param.split('_'))}"
                response["Location"] = f"/register/sign/up?message={message}"
                break
        else:
            # create a user
            new_user = User.objects.create_user(**details)
            new_user.save()

        return response
