import asyncio
import json

# from asgiref.sync import async_to_sync, sync_to_async  # Will be used for eventual consistency logic
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.decorators import login_required

from game.models import Player, Game
from helpers import authenticate_ws_connection, group_send

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await authenticate_ws_connection(self)
        # Add to group for this particular game
        self.group_name = self.scope["url_route"]["kwargs"]["game_id"]
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        await group_send(
            group_name=self.group_name, handler=data["handler"]
            , data=data)
        "If all players have joined, send game and positions with start time"
        "SO that everybody starts THAT TIME"

    async def playerMove(self, event):
        # Some database things...
        await self.default(event)

    async def playerUpdate(self, event):
        data = event["data"]["data"]
        player = await database_sync_to_async(Player.from_username)(data["username"])
        for field in data:
            setattr(player, field, data[field])
        await player.asave()
        await self.default(event)
        # PS: PLEASE Remember to await your coroutines when necessary - 'bug' took my time.

    async def start(self, event):
        await asyncio.sleep(1)  # Waiting for the last player's page to load...
        await self.default(event)

    async def default(self, event):
        """{
            data: {...},
            handler: "frontendFunctionName"
        }
        """
        await self.send(text_data=json.dumps(event["data"]))


    async def disconnect(self, close_code):
        # Leave game... group
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
    """
    Whenever the message start is received by the frontend, game = Game() is created, the message will come with the data and positions.
    The data will be stored in game, game stored in database
    The positions will be assigned to each player - 
    (Future version: What if a block can respawn after some time...)
    (It will now be person that breakes the most amount of block wins
    , since blocks do not really finish - It will be a Time Mode)
    (This one is classic mode.)
    """


class LoungeConsumer(AsyncWebsocketConsumer):
    """Consumer for the lounge, where people can see other people online."""
    async def connect(self):
        await authenticate_ws_connection(self)
        await self.channel_layer.group_add("lounge", self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave walk group
        await self.channel_layer.group_discard(
            "lounge", self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        # Later communicate with the backend
        # - Write to an error/data file to collect data
        # - Use in only one page
        pass

    # Receive message from walk group
    async def handle_frontend(self, event):
        event["data"]["message"] *= 3
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event["data"]))
    
    # default reception
    async def default(self, event):
        await self.send(text_data=json.dumps(event))
