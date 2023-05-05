"""
Routing file of channel layer (Web Socket)
"""

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

# from shared.middlewares.token_ws_auth_middleware import WebSocketTokenAuthenticationStack


websocket_urls = []


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket":
        URLRouter(
            websocket_urls
        )
    ,
})
