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
from helpers import make_game
from random import randint, sample, choice

base_path = "static/game/players/"

class Lounge(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = "lounge.html"
    model = Game
    fields = ["count", "max_hits"]

    def form_valid(self, form):
        player = self.request.user.player 
        if not player.game:
            player.game = form.save()
            player.save()
            msg.add_message(self.request, msg.SUCCESS, "You created and joined the game successfully")
            return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.player.game:
            context.update({
                "games": [game for game in Game.objects.all() if game.available]
            })
        return context

def create_game(request):
    message = ''
    player = Player.username(request)
    # check if a user is already in a game
    in_game = Game.objects.filter(pk=player.game, ended=False)
    # check if user has not played a created game
    created_not_played = Game.objects.filter(creator=player.user, started=False)
    print(player.user)
    if created_not_played:
        message = f"You already created game {created_not_played[0].pk}. "
    if in_game:
        message += f"Go back to game <a href=/game/{in_game[0].pk}>here</a>"
    if message:
        return HttpResponseRedirect(f"/lounge?message={message}")
    first_positions = []
    n_total = int(request.POST["nTotal"])
    n_bots = int(request.POST["nBots"])
    creator = request.user.username
    initial_data = json.dumps(make_game(15))
    while initial_data.count('0') < 15:
        initial_data = json.dumps(make_game(15)) # space for everybody
    data = json.loads(initial_data)
    # find all empty spaces *this should take a while
    for i, row in enumerate(data):
        index0 = 0
        while 0 in row[index0+1:]:
            index0 = row.index(0, index0+1)
            first_positions.append((0, i, index0))
    first_positions = sample(first_positions, n_total)
    # first_positions to be stored somewhere and
    # removed from
    game = Game(
          initial_data=initial_data,
          data=initial_data,
          n_bots=n_bots,
          n_real=n_total-n_bots,
          max_hits=int(request.POST["maxHits"]),
          creator=creator,
          )
    game.save()
    with open(f"{base_path}{game.pk}_players.json", 'w') as file:
        json.dump(first_positions, file)
    return HttpResponseRedirect(f"/lounge/?message={'game created successfully'}")

@login_required
def join_game(request, site):
    player = Player.username(request)
    game = Game.objects.filter(pk=site)
    if player.game:
        # could be this game
        return HttpResponseRedirect(f"/lounge?message={'You cannot join this game since you are already in one.'}")
        # make a function to do this, message will be an argument
    elif not game:
        return HttpResponseRedirect("/lounge?message=Invalid+Game")
    elif game[0].n_real == len(Player.objects.filter(game=site)):
        return HttpResponseRedirect(f"/lounge?message={'Game is full, choose to watch it instead'}")
    player.game = site
    # set position
    with open(f"{base_path}{game[0].pk}_players.json") as file:
        positions = json.load(file)
        for position in positions:
            if not position[0]: # not yet taken
                position[0] = player.user
                player.r, player.c = position[1:]
                print("got here", site, type(site))
                break
    with open(f"{base_path}{game[0].pk}_players.json", 'w') as file:
        json.dump(positions, file)
    player.save()
    return HttpResponseRedirect(f"/game/{site}")

# to implement 'watching' AIs + Me matches will have to be persisted (or indicated as non watchable)
# i.e if game.n_real == 1
