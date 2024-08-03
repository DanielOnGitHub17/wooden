import json
import os

from django.contrib import messages as msg
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic.edit import UpdateView

from game.models import Game, Player
from helpers import group_send_sync, make_game, WoodenError


class LeaveGame(LoginRequiredMixin, View):
    """
    Others can.
    """
    def post(self, request):
        player = request.user.player
        message = "You left the game successfully"
        if not player.game:
            message = "Error occured (nig)"
        elif player.game.started:
            message = "You need to stay in the game till it ends."
        elif player.creator and player.game.count == 1:
            message = "You can only leave if no one else has joined, start early instead."
        else:
            player.r = player.c = player.score = 0
            player.joined = player.present = False
            player.save()
        msg.add_message(request, msg.ERROR, message)    
        return redirect("/lounge/")

@login_required
def play(request):
    player = request.user.player
    game = player.game
    error_msg = (not game) * "You are not in a game.\n"
    error_msg = error_msg or (game.ended) * "You can no longer join that game."
    if error_msg:  # Can't join
        player.game = None
        player.save()
        msg.add_message(request, msg.ERROR, error_msg)
        return redirect("/lounge/")
    # Render game, socket and Consumers will create game and 
    # send data to all users so that JS can build it
    # It will send their positions to them too.
    # But first, let me do the waiting for them that will first trigger
    # Game.start()
    if not (player.joined and player.present):
        player.joined = player.present = True
        player.save()
    context = {
        "multiplayer": True,
        "players": {player.user.username: [player.joined, player.present] for player in game.players},
        "game": game,
        "game_data": game.try_start()
    }
    return render(request, "app/game.html", context)
    
class JoinGame(LoginRequiredMixin, View):
    def post(self, request):
        player = request.user.player
        if player.game:
            msg.add_message(request, msg.WARNING, "You are already in a game")
            return redirect("/play/")
        try:
            game_id = int(request.POST["game_id"])
            game = Game.objects.get(id=game_id)
            if game.available:
                player.game = game
                player.save()
                msg.add_message(request, msg.SUCCESS, "You joined the game successfully")
                # Send the "Gamer's" username, with event "createGamer"
                # Channel to all (Message will create an object on all player's platforms with joined=false, present=false)
                group_send_sync(group_name=game_id, data={"handler": "createGamer", "data": request.user.username})
        except:
            msg.add_message(request, msg.ERROR, "An error occured so you could not join the game")
        return redirect("/play/")

class EndGame(LoginRequiredMixin, View):
    def post(self, request):
        won = "won" in request.POST
        request.user.player.reset(won)
        if won:
            msg.add_message(request, msg.SUCCESS, "Congrats on winning that game! You've ranked up.")
        return redirect("/lounge/")

@login_required
def practice(request):
    return render(request, "app/game.html", {"game_data": make_game(10)})