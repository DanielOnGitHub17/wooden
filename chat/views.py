from django.shortcuts import render
from game.models import Player

def chat(request):
    online_players = Player.objects.all().order_by("won")
    context = {
        "online_players": online_players,
    }
    return render(request, "chat.html", context)