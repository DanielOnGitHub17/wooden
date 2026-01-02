# walk/routing.py
from django.urls import path

from . import consumers

websocket_urlpatterns = [
    # path("ws/lounge/", consumers.WalksConsumer.as_asgi()),
    path("ws/game/<str:game_id>/", consumers.GameConsumer.as_asgi()),
]
