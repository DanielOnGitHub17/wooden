"""Forms for the lounge app."""
from django import forms
from game.models import Game


class GameForm(forms.ModelForm):
    """Form for creating a game."""
    class Meta:
        """Meta class for GameForm."""
        model = Game
        fields = ["no_of_players", "wood_strength", "passcode"]
        widgets = {
            "no_of_players": forms.NumberInput(attrs={"min": 2, "max": 7}),
            "wood_strength": forms.NumberInput(attrs={"min": 2, "max": 7}),
            "passcode": forms.TextInput(attrs={
                "placeholder": "Passcode (optional)",
                "title": "Leave blank to create a public game",
                }),
        }
