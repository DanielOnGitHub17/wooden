from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request, user=""):
    # do things pertaining to user later
    return render(request, "homepage.html", {})