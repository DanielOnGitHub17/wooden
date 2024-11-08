import json

from django.contrib import messages as msg
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ValidationError
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.edit import CreateView

from game.models import Game, Player
from helpers import make_game, online_players_context
from random import randint, sample, choice


class Lounge(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = "app/lounge.html"
    model = Game
    fields = ["no_of_players", "max_hits"]

    def form_valid(self, form):
        player = self.request.user.player 
        if not player.game:
            player.game = form.save()
            player.creator = True
            player.save()
            msg.add_message(self.request, msg.SUCCESS, "You created and joined the game successfully")
            return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(online_players_context())
        if not self.request.user.player.game:
            context.update({
                "games": [game for game in Game.objects.all() if game.available]
            })
        return context

# to implement 'watching' AIs + Me matches will have to be persisted (or indicated as non watchable)
# i.e if game.n_real == 1
