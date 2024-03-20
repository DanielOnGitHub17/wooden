from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Game(models.Model):
    size = models.IntegerField(default=15)
    initial_data = models.TextField(default="0")
    data = models.TextField(default="0") # will change by json.loadsing and dumpsing
    max_hits = models.IntegerField(default=3)
    n_real = models.IntegerField(default=2)
    n_bots = models.IntegerField(default=2)
    started_time = models.DateTimeField(auto_now=True)
    ended_time = models.DateTimeField(auto_now=True)
    started = models.BooleanField(default=False)
    ended = models.BooleanField(default=False)
    creator = models.CharField(max_length=30)
    # will be used for 'leaderboarding' (maybe)
    winners = models.CharField(max_length=200)
    # primary key should be the link slash. (it will always change)
    def __str__(self):
        return f"Game {self.creator} {self.pk}"
    
    # The Game class will be frequently accessed by users, changed till there are no
    # '1s' in it's data.
    # if needed, the Game class will be turned to JSON later


    
class Player(models.Model):
    score = models.IntegerField(default=0)
    r = models.IntegerField(default=0)
    c = models.IntegerField(default=0)
    logged_in = models.BooleanField(default=False)
    user = models.CharField(max_length=30, primary_key=True)
    game = models.IntegerField(default=0)
    won = models.IntegerField(default=0)
    # will be given by difference between game.started and ended
    # (or game.started and logged out) Logout will have some work to do
    # it will have to check if the player was playing before he/she left
    # and other loopholes I will have to fill.

    def rank(self):
        me = Game.objects.filter
        return len(me(creator=self.user)) + 2*self.won

    def __str__(self):
        return f"Player {self.user}"
    
    @classmethod
    def username(self, request):
        return Player.objects.get(pk=request.user.username)


# should seamlessly connect to Game and User (or not)
# should change y and x on move.
# Player.objects.all() should do a lot.