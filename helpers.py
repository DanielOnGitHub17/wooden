from django.contrib.auth.models import User
from django.shortcuts import redirect
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

import sys
import os
from math import radians, cos, asin, sin, sqrt
from datetime import datetime
from importlib import reload

"""
These functions (and class) will help other portions of the code.
Some are generic, while others will be used at specific portions of the code.

Rules
 - Double quote for strings, single quotes for characters in Python, JS (as in C).
 - Document functions with comments at their top.

"""

# Constants
NEAR = 0.1
CHANNEL_LAYER = get_channel_layer()  # or maybe use channels "default" alias
dev_mails = ("dosuoha@gsumail.gram.edu", "enesidaniel.120064@gmail.com")

# Send message to a group
async def group_send(group_name="walks"
        , handler="handle_frontend"
        , data={}):
    await CHANNEL_LAYER.group_send(
        group_name, {"type": handler, "data": data}
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

# User.objects.
def delete_users():
    # I should probably just disable the accounts, not delete them.
    for x in User.objects.all():
        x.delete()

def callon_last(model, method="end"):
    getattr([*model.objects.all()][-1], method)()

# Show message in the browser by getting it from session
def show_message(request):
    message = ""
    if "message" in request.session:
        message = request.session["message"]
        request.session["message"] = ""
    return message
    
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
    raise error
    if redirect_to:
        return redirect(redirect_to)

# Faye's implementation of Haversine. Will help in checking proximity of locations.
def distance(lat1, long1, lat2, long2):
    # locations not points
    R = 6378

    lat1_rad = radians(lat1)
    lon1_rad = radians(long1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(long2)
    lat_diff = lat2_rad - lat1_rad
    lon_d = lon2_rad - lon1_rad

    a = sin(lat_diff / 2) * sin(lat_diff / 2) + cos(lat1_rad) * cos(lat2_rad) * sin(lon_d / 2) * sin(lon_d / 2)
    c = 2 * asin(sqrt(a))

    dist_km = R * c

    return dist_km

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
class WalkError(Exception): pass

# docker run --rm -p 6379:6379 redis:7: for running redis container.

if __name__ == "__main__":
    if len(sys.argv) == 2:
        if sys.argv[1] == "delete_all":
            delete_users()