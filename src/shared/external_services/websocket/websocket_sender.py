from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync, sync_to_async

from shared.constants.messages import *


class WebSocketSender:
    @classmethod
    def send_message(cls, group_name, message):
        data_event = {
            "event": "new_message",
            "message": message
        }
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            group_name, {
                'type': 'event.new.message',
                'data': data_event
            }
        )
