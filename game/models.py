"""The models of the game app - and logic that works on the database."""
import json

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone as tz

from helpers import group_send_sync, make_game, MAX_WAIT_TIME

def num_valid(x, y):
    """Validates the number of players and max hits."""
    return [MinValueValidator(x), MaxValueValidator(y)]

def validate_passcode_length(value):
    """Validates the length of the passcode."""
    if len(value) != 5:
        raise ValidationError('Passcode must be exactly 5 characters long.')

def validate_passcode_availability(value):
    """Validates the availability of the passcode."""
    if Game.objects.filter(passcode=value, ended=False).exists():  # pylint: disable=no-member
        raise ValidationError('Passcode already in use.')

# Create your models here.
class Game(models.Model):
    """The Game model."""
    size = models.IntegerField(default=15)
    initial_grid = models.TextField(default="")
    grid = models.TextField(default="")
    no_of_players = models.IntegerField(default=2, validators=num_valid(2, 7))
    max_hits = models.IntegerField(default=3, validators=num_valid(2, 7))
    started_time = models.DateTimeField(null=True)
    ended_time = models.DateTimeField(null=True)
    started = models.BooleanField(default=False)
    ended = models.BooleanField(default=False)
    passcode = models.CharField(max_length=5, null=True
                                , blank=True, validators=[
                                    validate_passcode_length
                                    ,validate_passcode_availability])
    # do passcode later for private games - join with passcode...
    # It will be so cool, the passcode becomes invalid when game starts

    def try_start(self, force=False):
        """Tries to start the game.
        If the game is not started and can be started, it starts the game."""
        game_data = {"hits": self.max_hits}
        if not self.started and (self.can_start or force):
            self.started = True
            game_data.update(
                make_game(users=[player.user.username for player in self.players])
            )
            self.initial_grid = self.grid = json.dumps(game_data["grid"])
            game_data["time"] = tz.now().timestamp() + MAX_WAIT_TIME
            self.started_time = tz.datetime.fromtimestamp(game_data["time"])
            for player in self.players:
                player.r, player.c = game_data["positions"][player.user.username]
                player.winner = False
                player.score = 0
                player.save()
            self.save()
            group_send_sync(group_name=self.pk, handler="start", data={
                "handler": "start", "data": game_data
            })
        elif self.ongoing:
            game_data.update(self.get_data())
        return game_data

    def get_data(self):
        """Returns the data of the game."""
        return {
            "grid": json.loads(self.grid),
            "positions": {player.user.username: (player.r, player.c) for player in self.players},
            "time": self.started_time.timestamp(),
        }

    def end(self):
        """Ends the game."""
        if not self.ended:
            self.ended = True
            self.save()

    @property
    def public(self):
        """Returns True if the game is public."""
        return self.passcode is None

    @property
    def available(self):
        """Returns True if the game is available for joining."""
        return not (self.started or self.ended or self.n == self.no_of_players)

    @property
    def ongoing(self):
        """Returns True if the game is ongoing."""
        return self.started and not self.ended

    @property
    def joined(self):
        """Returns the number of players who have joined the game."""
        return sum(player.joined for player in self.players)

    @property
    def players(self):
        """Returns the players of the game."""
        return Player.objects.filter(game=self)  # pylint: disable=no-member

    @property
    def n(self):
        """Returns the number of players in the game."""
        return len(self.players)

    def __str__(self):
        return f"Game {self.pk}"

    def get_absolute_url(self):
        """Returns the absolute url of the game."""
        return "/play/"

    @property
    def can_start(self):
        """Returns True if the game can be started."""
        return self.no_of_players == self.joined

    # The Game class will be frequently accessed by users, changed till there are no
    # '1s' in it's data.

class Player(models.Model):
    """The Player model."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    game = models.ForeignKey(Game, on_delete=models.PROTECT, null=True, blank=True)
    logged_in = models.BooleanField(default=False)
    score = models.IntegerField(default=0)
    r = models.IntegerField(default=0)
    c = models.IntegerField(default=0)
    winner = models.BooleanField(default=False)
    won = models.IntegerField(default=0)
    creator = models.BooleanField(default=False)
    # Socket needs
    joined = models.BooleanField(default=False)  # JOINED (checked once to see if joined)
    present = models.BooleanField(default=False)  # Paused (temporarily unavailable)/Resume

    @staticmethod
    def from_username(username):
        """Returns the player from the username."""
        return User.objects.get(username=username).player

    @property
    def rank(self):
        """Returns the rank of the player."""
        return 2*self.won

    @property
    def full_name(self):
        """Returns the full name of the player."""
        return self.user.get_full_name()  # pylint: disable=no-member

    def __str__(self):
        """Returns the string representation of the player."""
        return self.full_name

    def get_absolute_url(self):
        """Returns the absolute url of the player."""
        return f"/player/{self.pk}/"

    def reset(self, won=0, end=True):
        """Resets the player after the game ends."""
        if self.game and end:
            self.game.end()
        self.won += won
        self.game = None
        self.r = self.c = 0
        self.creator = self.joined = self.present = False
        self.save()
