from django.contrib import admin

from game.models import Game, Player

for model in (Game, Player):
    admin.site.register(model)
