"""This module contains the view for the lounge page."""

import requests

from django.contrib import messages as msg
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView

from django.conf import settings

from game.helpers import online_players_context
from game.models import Game
from lounge.forms import GameForm


class Lounge(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """View for the lounge page."""

    template_name = "app/lounge.html"
    model = Game
    form_class = GameForm
    # success_url = "/play/"

    def form_valid(self, form):
        player = self.request.user.player
        if player.game is not None:
            return None
        new_game: Game = form.save()
        player.game = new_game
        player.creator = True
        player.save()
        msg.add_message(
            self.request, msg.SUCCESS, "You created and joined the game successfully"
        )

        if settings.IS_HEROKU_APP or settings.USE_PROD_DATABASE:
            delete_url = getattr(settings, "DELETE_GAME_EXTERNAL_API_URL", None)
            if delete_url:
                payload = {"game_id": new_game.pk}
                try:
                    requests.post(delete_url, json=payload, timeout=5)
                except Exception:
                    pass

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(online_players_context())
        if not self.request.user.player.game:
            context.update(
                {
                    "games": [
                        game
                        for game in Game.objects.all()
                        if game.available and game.public
                    ]  # pylint: disable=no-member
                }
            )
        return context


# to implement 'watching' AIs + Me matches will have to be persisted (or indicated as non watchable)
# i.e if game.n_real == 1
# Try to implement Watching a game. Especially for private games.
