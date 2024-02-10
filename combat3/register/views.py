from django.shortcuts import render
from django.http import Http404
# Create your views here.

def register_page(request, which="up"):
    if which in ("up", "in"):
        return render(request, 'signs.html', {"which": which})
    else:
        raise Http404("Nothing here")

def signin(request):
    data = request.POST