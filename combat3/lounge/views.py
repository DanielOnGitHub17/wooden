from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User

# Create your views here.
@login_required
def lounge(request):
    online_users = []
    for user in User.objects.all():
        if user.username != "daniel":
            if user.is_authenticated:
                online_users.append(user)
                print(user.first_name)
            if user.is_active:
                
                print("active", user.first_name)

    # request.user is everything. (or most things). (or one third of things)
    return render(request, "lounge.html", {
        "user": request.user,
        "games": "get from the model",
        "online_users": online_users,
        "stats": "get from Player model"
    })

@login_required
def create_game(request):
    game = [type(request.POST[x]) for x in request.POST]
    return HttpResponse(str(game))