import datetime
import json

from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from helpers import group_send_sync, make_game

num_valid = lambda x, y: [MinValueValidator(x), MaxValueValidator(y)]

# Create your models here.
class Game(models.Model):
    size = models.IntegerField(default=15)
    initial_data = models.TextField(default="")
    data = models.TextField(default="") # will change by json.loadsing and dumpsing
    count = models.IntegerField(default=2, validators=num_valid(2, 7))
    max_hits = models.IntegerField(default=3, validators=num_valid(2, 7))
    started_time = models.DateTimeField(null=True)
    ended_time = models.DateTimeField(null=True)
    started = models.BooleanField(default=False)
    ended = models.BooleanField(default=False)
    # primary key should be the link slash. (it will always change)
    # do passcode later for private games - join with passcode...
    # It will be so cool, the passcode becomes invalid when game starts

    def try_start(self):
        if not self.started and self.joined == self.count:
            game_data = make_game(
                users=[player.user.username for player in self.players])
            self.game = json.dumps(game_data)
            self.started = True
            game_data["time"] = datetime.now().timestamp() + 20
            self.started_time = datetime.fromtimestamp(game_data["time"])
            self.save()
            return game_data
            

    @property
    def available(self):
        return not (self.started or self.ended or self.n == self.count)

    @property
    def ongoing(self):
        return self.started and not self.ended

    @property
    def joined(self):
        return sum(player.joined for player in self.players)

    @property
    def players(self):
        return Player.objects.filter(game=self)
    
    @property
    def n(self):
        return len(self.players)

    def __str__(self):
        return f"Game {self.pk}"
    
    def get_absolute_url(self):
        return f"/lounge/"
    
    @property
    def can_start(self):
        return all(player.joined for player in self.players)

    # The Game class will be frequently accessed by users, changed till there are no
    # '1s' in it's data.
    # if needed, the Game class will be turned to JSON later

class Player(models.Model):
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
    # For a user to join a game. The main thing should be to change the game attribute
    # will be given by difference between game.started and ended
    # (or game.started and logged out) Logout will have some work to do
    # it will have to check if the player was playing before he/she left
    # and other loopholes I will have to fill.

    @staticmethod
    def from_username(username):
        return User.objects.get(username=username).player

    @property
    def rank(self):
        return 2*self.won
    
    @property
    def full_name(self):
        return self.user.get_full_name()

    def __str__(self):
        return self.full_name
    
    def get_absolute_url(self):
        return f"/player/{self.id}/"
