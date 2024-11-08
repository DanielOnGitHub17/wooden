import os
import sys

from datetime import datetime
from importlib import import_module, reload
from random import choice, randint, sample

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect

"""
These functions (and class) will help other portions of the code.
Some are generic, while others will be used at specific portions of the code.

Rules
 - Double quote for strings, single quotes for characters in Python, JS (as in C).
 - Document functions with comments at their top.

"""

# Constants
CHANNEL_LAYER = get_channel_layer()  # or maybe use channels "default" alias
DEV_MAILS = (os.environ.get("EMAIL_HOST_USER"),)
MAX_WAIT_TIME = 10
username_prefixes = ("fighter", "runner", "quick", "super", "victorious",
                     "cool", "amazing", "fast", "smart", "kind", "big",
                       "powerful", "brave", "mighty", "potent")

# Function to generate suggested username to user.
def new_username(name): f"{choice(username_prefixes)}{name.capitalize()}{randint(10, 400)}"

# Get online players to be given to app views.
def online_players_context():
    from game.models import Player
    return {
        "online_players": Player.objects.filter(logged_in=True).order_by("-won"),
    }

# Resolve websocket_urlpatterns to be passed to asgi URLRouter
def join_wspatterns(paths):
    patterns = []
    for path in paths:
        for pattern in import_module(f"{path}.routing").websocket_urlpatterns:
            patterns.append(pattern)
    return patterns

# Send message to a group
async def group_send(group_name="lounge"
        , handler="default"
        , data={}):
    await CHANNEL_LAYER.group_send(
        str(group_name), {"type": handler, "data": data}
    )

# Copy of group_send for synchronous usage
group_send_sync = async_to_sync(group_send)

# To make email, which will be sent to devs
def make_email(request, email):
    user = request.user
    sender = full_name = "Unknown"
    if user.is_authenticated:
        sender = user.email
        full_name = user.get_full_name()
    return f"From {sender}. Name: {full_name}\n"\
           f"Message: {email}"

# Maze algorithm. 0, 1, 2. 0=space. 1=wood(breakable), 2=iron(protective)
def make_grid(dim=15):
    # set result to up and down borders
    return [
        [2] * (dim+2),
        *[
            *map(lambda x: [2]+list(map(lambda i: randint(0, 1), range(dim)))+[2], range(dim))
        ],
        [2] * (dim+2),
    ]

# Get zeros
def get_zeros(grid):
    return [(i, j) for j in range(1, 16) for i in range(1, 16) if not grid[i][j]]

# Make Game
def make_game(n=7, users=[]):
    n = len(users) or n
    zeros = []
    while len(zeros) < n:
        grid = make_grid()
        zeros = get_zeros(grid)
    zeros = sample(zeros, n)
    return {
        "grid": grid,
        "positions": {user: pos for user, pos in zip(users, zeros)}\
              if users else zeros,
    }

# User.objects.
def delete_users():
    # I should probably just disable the accounts, not delete them.
    for x in User.objects.all():
        x.delete()

def callon_last(model, method="end"):
    getattr([*model.objects.all()][-1], method)()

# Show message in the browser by getting it from session
# No need!!! use messages framework
    
# Could come in handy
def printurn(obj):
    print(obj)
    return obj

# Handle error by writing it into a file not present in the repo,
# printing it to the console, and redirecting if specified.
def handle_error(error, redirect_to=None):
    with open("../errors.log", 'a') as error_file:
        error_file.write(f"{error} | {datetime.now()}\n")
    print(error)
    # raise error
    if redirect_to:
        return redirect(redirect_to)

# Convert time to .pm/am string
def time_to_m(t):
    return t.strftime("%H:%M %p").lower()

# Function for changing events here to functions there
def as_frontend(event_type):
    parts = event_type.split('_')
    return parts[0].lower()+parts[1].capitalize()

# Clear the screen
def cls():
    os.system("cls") and os.system("clear")

# Generic Exception class for the app
class WoodenError(Exception): pass

# Mixin for Not login required
class NotLoginRequiredMixin(AccessMixin):
    """Redirect user if user is authenticated."""

    redirect_where = "/lounge/"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.redirect_where)
        return super().dispatch(request, *args, **kwargs)
# docker run --rm -p 5132:5132 redis:7: for running redis container.

if __name__ == "__main__":
    if len(sys.argv) == 2:
        if sys.argv[1] == "delete_all":
            delete_users()
