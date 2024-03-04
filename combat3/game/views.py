from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse

# Create your views here.
# from game.helpers import make_game
from game.models import Game
import json

@login_required
def play(request, site):
    # site will check model.
    
    message = "No game here"
    try:
        game = Game.objects.get(pk=site)
        waiting = False
        if not game.started:
            waiting = True
        elif game.ended:
            raise Exception("This game has ended, so you cannot watch it")
        else:
            can_play = (request.user.game == site)
            

        return render(request, "game.html", {
            "game": game,
            "can_play": can_play, # if can't play, you'll just watch.
            "waiting": waiting
        })
    except Exception as e:
        return HttpResponse(str(e))
    