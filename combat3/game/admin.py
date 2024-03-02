from django.contrib import admin

# Register your models here.
from game.models import Game
from game.models import Player

admin.site.register(Game)
admin.site.register(Player)