from django.apps import AppConfig
from django.contrib.auth.models import AnonymousUser

from shared.throttling.app import AppBaseThrottle
from shared.general_view import AppGeneralViewSet
# from shared.general_websocket_consumer import AsyncAppWebsocketConsumer
# from api.authentications.device_token_authentication import DeviceTokenAuthentication
from api.permissions.app import APIPermission
from api.containers import *


class ApiConfig(AppConfig):
    name = 'api'


class APIBaseViewSet(AppGeneralViewSet):
    # authentication_classes = (DeviceTokenAuthentication, )
    permission_classes = (APIPermission, )
    throttle_classes = (AppBaseThrottle,)
    throttle_scope = 'anonymous'

    # auth_service = auth_service
    # user_service = user_service
    # device_service = device_service
    # notification_service = notification_service
    # keys_service = keys_service
    # message_service = message_service
    # attachment_service = attachment_service
    # wallet_service = wallet_service
    # group_chat_service = group_chat_service
    # group_chat_member_service = group_chat_member_service

    def get_throttles(self):
        if self.request.user and not isinstance(self.request.user, AnonymousUser):
            self.throttle_scope = 'user_authenticated'
        else:
            self.throttle_scope = 'anonymous'
        return super(APIBaseViewSet, self).get_throttles()


# class APIBaseConsumer(AsyncAppWebsocketConsumer):
#     auth_service = auth_service
#     user_service = user_service
#     device_service = device_service
#     keys_service = keys_service
#     message_service = message_service
#     group_chat_service = group_chat_service
#     group_chat_member_service = group_chat_member_service
