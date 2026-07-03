"""
These functions (and class) will help other portions of the code.
Some are generic, while others will be used at specific portions of the code.

Rules
 - Double quote for strings, single quotes for characters (will have to give black formatter settings, or just leave it idk) in Python, JS (as in C).
 - Document functions with comments at their top.

"""

import os
import sys
import traceback
from datetime import datetime
from importlib import import_module

from asgiref.sync import async_to_sync
from channels.exceptions import DenyConnection
from channels.layers import get_channel_layer
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import redirect

# Constants
CHANNEL_LAYER = get_channel_layer()  # or maybe use channels "default" alias


def clear_temporary_players():
    """Clear users that didn't go through traditional sign in, clear inactive users"""
    # Go through all
    # Make sure they're not in a game that's active
    # Delete them


def unique_username(username):
    """checks if a username is unique - used for quick sign in"""
    if User.objects.filter(username=username):
        raise ValidationError("Username already exists!")


class WoodenError(Exception):
    """Generic exception class for the app."""


def join_wspatterns(paths):
    """Resolve websocket_urlpatterns to be passed to asgi URLRouter."""
    patterns = []
    for path in paths:
        for pattern in import_module(f"{path}.routing").websocket_urlpatterns:
            patterns.append(pattern)
    return patterns


async def group_send(group_name="lounge", handler="default", data=None):
    """Send message to a group."""
    await CHANNEL_LAYER.group_send(str(group_name), {"type": handler, "data": data})


# Copy of group_send for synchronous usage
group_send_sync = async_to_sync(group_send)


async def authenticate_ws_connection(consumer):
    """Authenticate WebSocket connection on consumer"""
    if not consumer.scope["user"].is_authenticated:
        raise DenyConnection("User not authenticated")


# To make email, which will be sent to devs
def make_email(request, email):
    """Make email to be sent to devs."""
    user = request.user
    sender = full_name = "Unknown"
    if user.is_authenticated:
        sender = user.email
        full_name = user.get_full_name()
    return f"From {sender}. Name: {full_name}\n" f"Message: {email}"


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

    with open("../errors.log", "a", encoding="utf-8") as error_file:
        error_file.write(error_message)

    print(error)
    # raise error
    if redirect_to is not None:
        return redirect(redirect_to)


def time_to_m(t):
    """Convert time to .pm/am string."""
    return t.strftime("%H:%M %p").lower()


def as_frontend(event_type):
    """Convert event type to frontend function."""
    parts = event_type.split("_")
    return parts[0].lower() + parts[1].capitalize()


def cls():
    """Clear the screen for windows and linux."""
    _ = os.system("cls") and os.system("clear")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        if sys.argv[1] == "delete_all":
            delete_users()
