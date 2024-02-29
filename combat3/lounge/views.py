from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
@login_required
def lounge(request):
    # request.user is everything. (or most things). (or one third of things)
    return render(request, "lounge.html", {
        "user": request.user,
        "games": "get from the model",
        "people": "get those online",
        "stats": "get from Player model"
    })

@login_required
def create_game(request):
    game = [type(request.POST[x]) for x in request.POST]
    return HttpResponse(str(game))