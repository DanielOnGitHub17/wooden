from django.shortcuts import render
from django.http import Http404\
    , HttpResponseRedirect, HttpResponsePermanentRedirect,\
    HttpResponse
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
        if "message" in request.GET:
            message = request.GET["message"]
        else:
            message = ''
        context = {
            "form": form,
            "which": get_which(which),
            "message": message,
        }
        return render(request, 'signs.html', context)
    else:
        raise Http404("Nothing here")

class Log(View):
    def get(self, request):
        user = request.GET
        response = HttpResponse(status=302)
        # response = HttpResponse(status=302, headers={"message": "Daniel"})
        try:
            player = Player.objects.get(pk=user["username"])
            if player.password == user["password"]:
                response["Location"] = "/lounge"
            else:
                raise PermissionError("Wrong Password")
        except Exception as e:
            response["X-message"] = "Invalid username or wrong password"
            response["Location"] = f"/register/sign/in?message={response["X-message"]}"
        return response
        
    
    def post(self, request):
        # if request.POST
        new_user = SignForm(request.POST)
        if new_user.is_valid():
            new_user.save()
            return HttpResponseRedirect("/register/sign/in")
        else:
            message = "Invalid credentials."
            return HttpResponse("/register/sign/up?message={message}")
