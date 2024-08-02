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
from lounge.views import base_path

class LeaveGame(LoginRequiredMixin, View):
    pass

class EndGame(LoginRequiredMixin, View):
    def post(self, request):
        request.user.player.reset("won" in request.POST)
        return redirect("/lounge/")
        

class GamePlay(LoginRequiredMixin, View):
    def post(self, request):
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
        return render(request, "game_temp.html", context)        

    def get(self, request):
        return render(request, "game_temp.html", {"game_data": make_game(10)})
    
    
class JoinGame(LoginRequiredMixin, View):
    def post(self, request):
        player = request.user.player
        if player.game:
            msg.add_message(request, msg.WARNING, "You are already in a game")
            return redirect("/lounge/")
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
        return redirect("/lounge/")
