from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Game(models.Model):
    size = models.IntegerField()
    max_hits = models.IntegerField()
    n_real = models.IntegerField()
    n_bots = models.IntegerField()
    started = models.DateTimeField(auto_now=True)
    ended = models.DateTimeField()
    creator = models.IntegerField()
    # will be used for 'leaderboarding' (maybe)
    winner = models.IntegerField()
    # primary key should be the link slash. (it will always change)


    
class Player(models.Model):
    score = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    x = models.IntegerField(default=0)
    logged_in = models.BooleanField(default=True)
    user = models.CharField(max_length=90)
    game = models.IntegerField(default=0)
    # will be given by difference between game.started and ended
    # (or game.started and logged out) Logout will have some work to do
    # it will have to check if the player was playing before he/she left
    # and other loopholes I will have to fill.


# should seamlessly connect to Game and User (or not)
# should change y and x on move.
# Player.objects.all() should do a lot.