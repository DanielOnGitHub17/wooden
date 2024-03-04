import json

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from game.models import Game, Player
from random import randint, sample
from game.helpers import make_game


# Create your views here.
@login_required
def lounge(request):
    online_users = [*Player.objects.filter(logged_in=True)]
    games_to_join = [*Game.objects.filter(started=False, ended=False)]
    ongoing_games = [*Game.objects.filter(started=True, ended=False)]
    message = request.GET["message"] if "message" in request.GET else '' 
    return render(request, "lounge.html", {
        "user": request.user,
        "games": [games_to_join, ongoing_games],
        "online_users": online_users,
        "stats": "get from Player model",
        "message": message # JS can actually handle this
    })

@login_required
def create_game(request):
    # check if a user is already in a game
    in_game = Game.objects.filter(pk=request.user.game)
    if in_game:
        message = f"You are already in game {in_game[0].pk}.\
              You can go back <a href=f'/game/{in_game[0].pk}'>here</a>"
        HttpResponseRedirect(f"/lounge?message={message}")
    first_positions = []
    n_total = int(request.POST["nTotal"])
    n_bots = int(request.POST["nBots"])
    creator = request.user.username
    print(type(n_total))
    initial_data = json.dumps(make_game(15))
    while initial_data.count('0') < 15:
        initial_data = json.dumps(make_game(15)) # space for everybody
    data = json.loads(initial_data)
    # find all empty spaces *this should take a while
    for i, row in enumerate(data):
        while index0+1:
            first_positions.append((index0,i)) # x, y
            index0 = row.find(0)
    first_positions = sample(first_positions, n_total)
    # first_positions to be stored somewhere and
    # removed from
    game = Game(
          initial_data=initial_data,
          data=initial_data,
          n_bots=n_bots,
          n_real=n_total-n_bots,
          max_hits=int(request.GET["maxHits"]),
          creator=creator,
          )
    game.save()
    with open(f"game{game.pk}_players.json", 'w') as file:
        json.dump(first_positions, file)
    creator = Player.objects.get(pk=creator)
    creator.game = game.pk
    creator.save()
    return HttpResponseRedirect(f"/game/{game.pk}") # game will say "waiting for players"