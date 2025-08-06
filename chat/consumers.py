import json
import time

from helpers import AuthenticateAsyncWebSocketConsumer

class ChatConsumer(AuthenticateAsyncWebSocketConsumer):
    async def connect(self):
        await super().authenticate()
        await self.channel_layer.group_add("chat", self.channel_name)
        await self.accept()
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        # Check data message [1], if it is bad, change it to "[BLOCKED]"
        # Maybe block [0] if it is bad.
        # Broadcast chat to all.
        await self.channel_layer.group_send(
            "chat", {"type": "chat.message", "data": json.dumps(data)}
        )

    async def chat_message(self, event):
        await self.send(text_data=event["data"])

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "chat", self.channel_name
        )

