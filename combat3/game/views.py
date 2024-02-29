from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
from game.helpers import make_game

@login_required
def game(request, site=''):
    # check if request is valid, ..., then finally
    # make_game(request.GET["dim"])
    # site will check model .
    return render(request, "game.html", {"game": make_game(15)})