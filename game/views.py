import json
import os

import json

from django.contrib import messages as msg
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.edit import UpdateView

from game.models import Game, Player
from helpers import make_game, WoodenError
from lounge.views import base_path


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
        player.joined = player.present = True
        player.save()  # Save will channel
        context = {
            "multiplayer": True,
            "players": {player.user.username: [player.joined, player.present] for player in game.players}
        }
        return render(request, "game_temp.html", context)
        
        """
        When everybody joins, the data and positions are created and stored.
        The GAME is created when everybody joins (
        and there could also be a start early button that can start once more than one person joined)
        The data will be stored in a JSON file. The changes to the file
        , as well as data to other, will be tracked later for ML
        Events for socket:
        Player JOINED - if the player joined successfully but has no position
        Player Paused - if, player window is unfocused/player not sending input/sth.
        Player Resumed - if, you get. (could be to sharpen a blured player name/check an 'available' box)
        Player LEFT - if, NAVIGATED out of game / logged out.
          (Blurring window doesn't count...), this will be for later
        Game Started - when all users have JOINED (I might have to add more fields in DB)
        Game Ended - when blocks are all cleared
        Ping might affect these events, of course.
        Also, no one can join once they leave - game becomes 'unavailable'
        """

        

    def get(self, request):
        game = make_game()
        context = {"game": game}
        return render(request, "game_temp.html", context)
    
    
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
        except:
            msg.add_message(request, msg.ERROR, "An error occured so you could not join the game")
        return redirect("/lounge/")

@login_required
# Update view to start  game by updating game data
class StartGame:
    # grid = make_game()
    #         zeros = []
    #         while len(zeros) < 15:
    #             zeros = [(i, j) for j in range(1, 16) for i in ran]ge(1, 16) if not grid[i][j]]
    #         sample(zeros, ...)
            # Do all these later. Do them in the game app - it will happen
            # when the game is about to start, it will be the 'loading'
            # I might not even store the data at all -> until after the game
            # This will just create the game as an object with data default='0'
            # It should be easier, like, I will be 'sharing'
            # Maybe I could pickle the grid...
            # Make the game grid, a 15 by 15 matrix
            
    pass

@login_required
def play(request, site):
    # site will check model.

    message = "No game here"
    try:
        game = Game.objects.get(pk=site)
        # if game has ended, just leave
        if game.ended:
            raise Exception("This game has ended, so you can neither play nor watch it.")
        with open(f"{base_path}{game.pk}_players.json") as file:
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
                os.remove(f"{base_path}{game.pk}_players.json")
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

# for the player immediate communication.
# maybe join all to one.
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
    return HttpResponse("failed")

@login_required
def crack(request):
    # can be hacked by just inputing the url in a browser window correctly
    game_id = Player.username(request).game
    if game_id and 'r' in request.GET and 'c' in request.GET:
        r, c = [int(request.GET[x]) for x in ('r', 'c')]
        game = Game.objects.get(pk=game_id)
        data = json.loads(game.data)
        data[r][c] = 0 # cracking
        game.data = json.dumps(data)
        game.save()
        return HttpResponse('')
    print("failed")
    return HttpResponse("failed")