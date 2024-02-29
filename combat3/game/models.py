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
    winner = models.ForeignKey(User, on_delete=models.CASCADE)  # will be used for 'leaderboarding' (maybe)
    # primary key should be the link slash. (it will always change)


    
class Player(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    current_game = models.ForeignKey(Game, on_delete=models.CASCADE)
    score = models.IntegerField()
    y = models.IntegerField()
    x = models.IntegerField()


# should seamlessly connect to Game and User
# should change y and x on move.
# Player.objects.all() should do a lot.