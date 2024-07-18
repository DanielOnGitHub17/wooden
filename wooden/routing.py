from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from game.routing import websocket_urlpatterns  # Import the app-level routing

channel_routing = {
    'websocket': URLRouter(websocket_urlpatterns),
}
