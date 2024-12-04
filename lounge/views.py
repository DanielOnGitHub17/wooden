"""This module contains the view for the lounge page."""
# import json

from django.contrib import messages as msg
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView


from game.models import Game
from lounge.forms import GameForm
from helpers import online_players_context


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
        player.game = form.save()
        player.creator = True
        player.save()
        msg.add_message(self.request, msg.SUCCESS
                        , "You created and joined the game successfully")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(online_players_context())
        if not self.request.user.player.game:
            context.update({
                "games": [game for game in Game.objects.all()\
                           if game.available and game.passcode == ""]  # pylint: disable=no-member
            })
        return context

# to implement 'watching' AIs + Me matches will have to be persisted (or indicated as non watchable)
# i.e if game.n_real == 1
# Try to implement Watching a game. Especially for private games.
