from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse

import os

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
    
@login_required
def end_game(request):
    player = Player.username(request)
    if "GAME" in request.GET:
        print("Game in")
        if player.game == int(request.GET["GAME"]):
            # end game
            game = Game.objects.get(pk=player.game)
            max_score = max(gamer.score for gamer in Player.objects.filter(game=player.game))
            # might have to add a "game over" to Player model
            print("max_score", player.user, max_score)
            if not game.ended:
                game.ended = True
                game.winners =  ' '.join(gamer.user \
                        for gamer in Player.objects.filter(game=player.game, score=max_score))
                os.remove(f"game/static/game{game.pk}_players.json")
                game.save()
            return back_to_lounge(request, player, max_score)
    print("jkj")
    return redirect("/lounge")

@login_required
def back_to_lounge(request, player, max_score):
    print(player.score)
    if player.game == 0: # has passed through this function once
        return redirect("/lounge")
    if player.score == max_score:
        player.won += 1
        message = f"You won game {player.game} with a score of {player.score}"
    else:
        message = f"You did not win game {player.game}. Your score is {player.score}. The highest score was {max_score}."

    player.r = player.c = player.score = player.game = 0
    player.save()
    print(f"Took {player.user} back to lounge")
    return redirect(f"/lounge?message={message}")

# for the player immediate communication
@login_required
def score(request):
    if "score" in request.GET:
        player = Player.username(request)
        player.score = int(request.GET["score"])
        player.save()
        return HttpResponse(request.GET["score"])
    return HttpResponse("failed")

@login_required
def pos(request):
    if 'r' in request.GET and 'c' in request.GET:
        player = Player.username(request)
        player.r, player.c = request.GET['r'], request.GET['c']
        player.save()
        return HttpResponse('')
    return HttpResponse("failed")

@login_required
def position(request):
    # instead of constantly calling this, there should be a
    # connection that says WHEN to call this, that whenever position
    # is set by others, this is called by others except others.
    if "player" in request.GET:
        player = Player.objects.get(user=request.GET["player"])
        return HttpResponse(f"{[player.r, player.c]}")
    return HttpResponse('failed')
    

# @login_required
# def check_can_start(request):
#     game_id = request.GET[""]
#     game_id*2