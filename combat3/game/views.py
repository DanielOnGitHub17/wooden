from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse

# Create your views here.
# from game.helpers import make_game
from game.models import Game, Player
import json

@login_required
def play(request, site):
    # site will check model.
    
    message = "No game here"
    try:
        game = Game.objects.get(pk=site)
        # if game has ended, just leave
        if game.ended:
            raise Exception("This game has ended, so you can neither play nor watch it.")
        with open(f"game/static/game{game.pk}_players.json") as file:
            positions = json.load(file)
        # game has started if enough players have joined
        n_players = len(Player.objects.filter(game=game.pk))
        game.started = game.n_real == n_players
        if game.started: # don't want to call .save too much.
            game.save()
        can_play = (Player.username(request).game == site)

        return render(request, "game.html", {
            "game": game,
            "can_play": can_play, # if can't play, you'll just watch.
            "n_players": n_players,
            "positions": positions,
        })
    except Exception as e:
        return HttpResponse(str(e))
    
# @login_required
# def check_can_start(request):
#     game_id = request.GET[""]
#     game_id*2