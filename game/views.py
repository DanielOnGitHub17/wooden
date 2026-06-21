"""Views for the game app."""

import json
from django.contrib import messages as msg
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect, render
from django.views import View

from django.conf import settings

from game.helpers import make_game, DEFAULT_GRID_SIZE
from game.models import Game
from helpers import WoodenError, group_send_sync, handle_error


class ChangeToPublic(LoginRequiredMixin, View):
    """View for changing a game to public."""

    def post(self, request: HttpRequest):
        """Change a game to public."""
        player = request.user.player
        game = player.game
        if game and game.available and not game.public and player.creator:
            game.passcode = None
            game.save()
            return HttpResponse(status=200)
        return HttpResponse(status=400)


class LeaveGame(LoginRequiredMixin, View):
    """View for leaving a game."""

    def post(self, request: HttpRequest):
        """Leave a game."""
        player = request.user.player
        game = player.game
        message, next_ = "You left the game successfully", "/play/"
        if not game:
            message = "Error occured (NIG)"
        elif game.ongoing:
            message = "You need to stay in the game till it ends."
        elif player.creator and game.joined > 1:
            message = (
                "You can only leave if no one else has joined, start early instead."
            )
        else:
            message = "Sorry you could not wait! Make a game/join one below."
            player.reset(end=player.creator)
            next_ = "/lounge/"
            # Tell other players.
            group_send_sync(
                group_name=game.id,
                data={"handler": "playerLeave", "data": request.user.username},
            )

        msg.add_message(request, msg.ERROR, message)
        return redirect(next_)


class StartEarly(LoginRequiredMixin, View):
    """View for starting a game early."""

    def post(self, request: HttpRequest):
        """Start a game early."""
        player = request.user.player
        game = player.game
        if not game:
            msg.add_message(request, msg.ERROR, "SERVER ERROR (NIG).")
            return redirect("/lounge/")
        elif not player.creator:
            msg.add_message(request, msg.ERROR, "You are not the creator of this game.")
            return redirect("/play/")
        elif game.joined < 2:
            msg.add_message(
                request, msg.ERROR, "You need at least 2 players to start the game."
            )
            return redirect("/play/")

        # Change the number of players required to start the game
        game.no_of_players = game.joined
        game.save()
        msg.add_message(request, msg.SUCCESS, "Game will start soon.")
        return redirect("/play/")


@login_required
def play(request: HttpRequest):
    """View for playing a game."""
    player = request.user.player
    game: Game = player.game
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
        "players": {
            player.user.username: [player.joined, player.present]
            for player in game.players
        },
        "game": game,
        "game_data": game.try_start(),
    }

    return render(request, "app/game.html", context)


class JoinGame(LoginRequiredMixin, View):
    """View for joining a game."""

    def post(self, request: HttpRequest):
        """Join a game."""
        player = request.user.player
        redirect_to = "/lounge/"
        if player.game:
            msg.add_message(request, msg.WARNING, "You are already in a game")
            return redirect("/play/")
        try:
            # This could trigger the DoesNotExist exception
            passcode = request.POST.get("passcode", "")
            if passcode:
                game = [
                    game_obj
                    for game_obj in Game.objects.filter(passcode=passcode)
                    if game_obj.available
                ][
                    0
                ]  # pylint: disable=no-member
                game_id = game.id
            else:
                game_id = int(request.POST["game_id"])
                game = Game.objects.get(id=game_id)  # pylint: disable=no-member
            if not game.available:
                raise WoodenError("Game is not available to join")
            player.game = game
            player.save()
            msg.add_message(request, msg.SUCCESS, "You joined the game successfully")
            # Send the "Gamer's" username, with event "createGamer"
            # Channel to all (Message will create an object on
            #    all players' platforms with joined=false, present=false)
            group_send_sync(
                group_name=game_id,
                data={"handler": "createGamer", "data": request.user.username},
            )
            redirect_to = "/play/"
        except IndexError:
            msg.add_message(request, msg.ERROR, "Oops! That passcode is incorrect.")
        except Game.DoesNotExist:  # pylint: disable=no-member
            msg.add_message(
                request, msg.ERROR, "Oops! That game does not exist. (NiceTryHacker)"
            )
        except WoodenError as e:
            msg.add_message(request, msg.ERROR, str(e))
        except Exception as e:  # pylint: disable=broad-except
            handle_error(e)
            msg.add_message(
                request, msg.ERROR, "An error occured so you could not join the game"
            )
        return redirect(redirect_to)


class EndGame(LoginRequiredMixin, View):
    """View for ending a game."""

    def post(self, request: HttpRequest):
        """End a game."""
        won = +("won" in request.POST)
        request.user.player.reset(won)
        msg.add_message(
            request,
            msg.SUCCESS,
            [
                "Sorry about losing that game. Do better next time.",
                "Congrats on winning that game! You've ranked up.",
            ][won],
        )
        return redirect("/lounge/")


class DeleteGame(View):
    """API to delete a game."""

    def get(self, request: HttpRequest):
        """Delete a game by id using a JSON payload."""
        game_id = request.GET.get("game_id")
        print("request", request.GET.get("DELETE_GAME_TOKEN"))
        print("truth", settings.DELETE_GAME_TOKEN)
        if request.GET.get("DELETE_GAME_TOKEN") != getattr(
            settings, "DELETE_GAME_TOKEN", None
        ):
            return HttpResponse(content=b"Invalid delete token", status=403)

        try:
            game = Game.objects.get(id=game_id)
        except (Game.DoesNotExist, TypeError, ValueError):
            return HttpResponse(content=b"Game not found", status=404)

        self.delete_game(game)
        return HttpResponse(status=200)

    @staticmethod
    def delete_game(game: Game):
        """Reset players in the game and delete it."""
        for player in game.players.all():
            player.reset(end=False)
        game.delete()


# @login_required
def practice(request: HttpRequest):
    """View for practicing a game."""
    dimension = int(request.GET.get(settings.GRID_SIZE_SETTER, DEFAULT_GRID_SIZE))
    return render(
        request,
        "app/game.html",
        {"game_data": make_game(dimension=dimension)},
    )
