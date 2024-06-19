from django.forms import ModelForm
from game.models import Game

class GameForm(ModelForm):
    class Meta:
        model = Game
        fields = ["max_hits", "n_real", "n_bots"]