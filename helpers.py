"""
These functions (and class) will help other portions of the code.
Some are generic, while others will be used at specific portions of the code.

Rules
 - Double quote for strings, single quotes for characters in Python, JS (as in C).
 - Document functions with comments at their top.

"""

import os
import sys
import traceback

from datetime import datetime
from importlib import import_module  # type: ignore
from random import choice, randint, sample

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect


import requests as req

# Load environment variables from .env during development
# from dotenv import load_dotenv
# load_dotenv()

# Constants
CHANNEL_LAYER = get_channel_layer()  # or maybe use channels "default" alias
DEV_MAILS = (os.environ.get("EMAIL_HOST_USER"),)
MAX_WAIT_TIME = 10
username_prefixes = ("fighter", "runner", "quick", "super", "victorious",
                     "cool", "amazing", "fast", "smart", "kind", "big",
                       "powerful", "brave", "mighty", "potent")

def new_username(name):
    """Generate a new username for the user."""
    return f"{choice(username_prefixes)}{name.capitalize()}{randint(10, 400)}"

def online_players_context():
    """Get online players to be given to app views."""
     # To avoid circular import
    from game.models import Player  #  pylint: disable=import-outside-toplevel
    return {
        "online_players": Player.objects.filter(logged_in=True).order_by("-won"),  # pylint: disable=no-member
    }

def join_wspatterns(paths):
    """Resolve websocket_urlpatterns to be passed to asgi URLRouter."""
    patterns = []
    for path in paths:
        for pattern in import_module(f"{path}.routing").websocket_urlpatterns:
            patterns.append(pattern)
    return patterns

async def group_send(group_name="lounge"
        , handler="default"
        , data=None):
    """Send message to a group."""
    await CHANNEL_LAYER.group_send(
        str(group_name), {"type": handler, "data": data}
    )

# Copy of group_send for synchronous usage
group_send_sync = async_to_sync(group_send)

# To make email, which will be sent to devs
def make_email(request, email):
    """Make email to be sent to devs."""
    user = request.user
    sender = full_name = "Unknown"
    if user.is_authenticated:
        sender = user.email
        full_name = user.get_full_name()
    return f"From {sender}. Name: {full_name}\n"\
           f"Message: {email}"

# Maze algorithm. 0, 1, 2. 0=space. 1=wood(breakable), 2=iron(protective)
def make_grid(dim=15):
    """Make a grid for the game."""
    # set result to up and down borders
    return [
        [2] * (dim+2),
        *[
            *map(lambda x: [2]+list(map(lambda i: randint(0, 1), range(dim)))+[2], range(dim))
        ],
        [2] * (dim+2),
    ]

def get_zeros(grid):
    """Get zeros from the grid."""
    return [(i, j) for j in range(1, 16) for i in range(1, 16) if not grid[i][j]]

def make_game(n=7, users=None):
    """Make a game for the users."""
    if users is None:
        users = []
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

def delete_users():
    """Delete all users."""
    # I should probably just disable the accounts, not delete them.
    for x in User.objects.all():
        x.delete()

def callon_last(model, method="end"):
    """Call a method on the last object of a model."""
    getattr([*model.objects.all()][-1], method)()

# Show message in the browser by getting it from session
# No need!!! use messages framework

# Could come in handy
def printurn(obj):
    """Print and return an object."""
    print(obj)
    return obj

def handle_error(error, redirect_to=None):
    """Handle error by writing it into a file
    , printing it to the console, and redirecting if specified.
    Format for ease of parsing. .split("ERROR>>>").split('|').stripforeach...
    """
    error_details = traceback.format_exc()
    error_message = f"ERROR>>> {datetime.now()} | {error} |\n{error_details}\n"

    with open("../errors.log", 'a', encoding="utf-8") as error_file:
        error_file.write(error_message)

    print(error)
    # raise error
    if redirect_to:
        return redirect(redirect_to)

def time_to_m(t):
    """Convert time to .pm/am string."""
    return t.strftime("%H:%M %p").lower()

def as_frontend(event_type):
    """Convert event type to frontend function."""
    parts = event_type.split('_')
    return parts[0].lower()+parts[1].capitalize()

def cls():
    """Clear the screen for windows and linux."""
    os.system("cls") and os.system("clear")  # pylint: disable=expression-not-assigned

class WoodenError(Exception):
    """Generic exception class for the app."""

class NotLoginRequiredMixin(AccessMixin):
    """Redirect user if user is authenticated.
    Mixin for Not login required
    """

    redirect_where = "/lounge/"

    def dispatch(self, request, *args, **kwargs):
        """Dispatch method for the class."""
        if request.user.is_authenticated:
            return redirect(self.redirect_where)
        return super().dispatch(request, *args, **kwargs)

def verify_recaptcha(token):
    """Verify recaptcha token."""
    response = req.post(
        "https://www.google.com/recaptcha/api/siteverify",
        data={
            "secret": os.getenv("RECAPTCHA_SECRET_KEY"),
            "response": token,
        },
    )
    return response.json().get("success", False)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        if sys.argv[1] == "delete_all":
            delete_users()
