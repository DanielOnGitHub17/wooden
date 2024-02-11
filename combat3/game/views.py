from django.shortcuts import render

# Create your views here.
from helpers import make_game

def game(request):
    # check if request is valid, ..., then finally
    # make_game(request.GET["dim"])
    return render(request, "game.html", {"game": make_game(5)})