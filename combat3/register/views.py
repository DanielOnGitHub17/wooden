from django.shortcuts import render
from django.http import Http404\
    , HttpResponseRedirect, HttpResponsePermanentRedirect
from django.views import View

from register.forms import SignForm
from register.models import Player

# Create your views here.

def get_which(which):
    return {
        "up": ("POST", "Create an account", "Create Account"),
        "in": ("GET", "Log into your combat account", "Log in"),
     }[which]

def register_page(request, which="up"):
    if which in ("up", "in"):
        form = SignForm()
        with open("headers.txt", 'w') as file:
            file.write('\n'.join(f"{key}: {request.META[key]}" for key in request.META))
        if "MESSAGE" in request.META:
            print("MESSAGEing")
            MESSAGE = request.META["MESSAGE"]
        else:
            MESSAGE = ''
        context = {
            "form": form,
            "which": get_which(which),
            "MESSAGE": MESSAGE,
        }
        return render(request, 'signs.html', context)
    else:
        raise Http404("Nothing here")

class Log(View):
    def get(self, request):
        user = request.GET
        try:
            player = Player.objects.get(pk=user["username"])
            if player.password == user["password"]:
                return HttpResponsePermanentRedirect("/lounge")
        except Player.DoesNotExist:
            response = HttpResponseRedirect("/register/sign/in")
            response.headers["MESSAGE"] = f"Invalid username or wrong password"
            return response

        
    
    def post(self, request):
        # if request.POST
        new_user = SignForm(request.POST)
        if new_user.is_valid():
            new_user.save()
        return HttpResponseRedirect("/register/sign/in")

