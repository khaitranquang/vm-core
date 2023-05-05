"""
ASGI entrypoint. Configures Django and then runs the application
defined in the ASGI_APPLICATION setting.
"""

import os

import django
from channels.routing import get_default_application


valid_env = ['prod', 'env', 'staging']
env = os.getenv("PROD_ENV")
if env not in valid_env:
    env = 'dev'

setting = "server_config.settings.%s" % env
os.environ.setdefault("DJANGO_SETTINGS_MODULE", setting)
django.setup()

application = get_default_application()


# import os
#
# from channels.routing import ProtocolTypeRouter, URLRouter
# from django.core.asgi import get_asgi_application
#
# from shared.middlewares.token_ws_auth_middleware import WebSocketTokenAuthenticationStack
# from api.websocket import urls as v1_websocket_urls
#
#
# websocket_urls = []
# websocket_urls += v1_websocket_urls.websocket_urlpatterns
#
# valid_env = ['prod', 'env', 'staging']
# env = os.getenv("PROD_ENV")
# if env not in valid_env:
#     env = 'dev'
#
# setting = "server_config.settings.%s" % env
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', setting)
#
#
# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": WebSocketTokenAuthenticationStack(
#         URLRouter(
#             websocket_urls
#         )
#     ),
# })
