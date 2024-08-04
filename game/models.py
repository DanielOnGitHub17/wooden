import json

# from asgiref.sync import ync_to_async
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone as tz
from helpers import group_send, group_send_sync, make_game, MAX_WAIT_TIME

num_valid = lambda x, y: [MinValueValidator(x), MaxValueValidator(y)]

# Create your models here.
class Game(models.Model):
    size = models.IntegerField(default=15)
    initial_grid = models.TextField(default="")
    grid = models.TextField(default="")
    count = models.IntegerField(default=2, validators=num_valid(2, 7))
    max_hits = models.IntegerField(default=3, validators=num_valid(2, 7))
    started_time = models.DateTimeField(null=True)
    ended_time = models.DateTimeField(null=True)
    started = models.BooleanField(default=False)
    ended = models.BooleanField(default=False)
    # do passcode later for private games - join with passcode...
    # It will be so cool, the passcode becomes invalid when game starts

    def try_start(self, force=False):
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
            group_send_sync(group_name=self.id, handler="start", data={
                "handler": "start", "data": game_data
            })
        elif self.ongoing:
            game_data.update(self.get_data())
        return game_data

    def get_data(self):
        return {
            "grid": json.loads(self.grid),
            "positions": {player.user.username: (player.r, player.c) for player in self.players},
            "time": self.started_time.timestamp(),
        }
    
    def end(self):
        if not self.ended:
            self.ended = True
            self.save()

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
        return "/play/"
    
    @property
    def can_start(self):
        return self.count == self.joined

    # The Game class will be frequently accessed by users, changed till there are no
    # '1s' in it's data.

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
    
    def reset(self, won=0, end=True):
        if self.game and end:
            self.game.end()
        self.won += won
        self.game = None
        self.r = self.c = 0
        self.creator = self.joined = self.present = False
        self.save()
