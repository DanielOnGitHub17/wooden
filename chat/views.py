from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from helpers import online_players_context

@login_required
def chat(request):
    return render(request, "app/chat.html", online_players_context())