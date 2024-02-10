from django.shortcuts import render
from django.http import Http404\
    , HttpResponseRedirect, HttpResponsePermanentRedirect
from django.views import View

from register.forms import SignForm

# Create your views here.

def get_which(which):
    return {
        "up": ("POST", "Create an account", "Create Account"),
        "in": ("GET", "Log into your combat account", "Log in"),
     }[which]

def register_page(request, which="up"):
    if which in ("up", "in"):
        form = SignForm()
        context = {
            "form": form,
            "which": get_which(which),
        }
        return render(request, 'signs.html', context)
    else:
        raise Http404("Nothing here")

class Log(View):
    def get(self, request):
        return HttpResponsePermanentRedirect("/lounge")
    
    def post(self, request):
        # if request.POST
        new_user = SignForm(request.POST)
        if new_user.is_valid():
            new_user.save()
        return HttpResponseRedirect("/register/sign/in")

