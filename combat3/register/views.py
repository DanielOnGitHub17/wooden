from django.shortcuts import render
from django.http import Http404\
    , HttpResponseRedirect, HttpResponsePermanentRedirect,\
    HttpResponse
from django.views import View

# Create your views here.

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
        details = request.GET
        pass
        
    
    def post(self, request):
        details = request.POST
        pass
