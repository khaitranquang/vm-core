import json
from channels.generic.websocket import AsyncWebsocketConsumer

from django.contrib.auth.models import AnonymousUser

from shared.error_responses.error import gen_error, refer_error
from shared.log.cylog import CyLog


class AsyncAppWebsocketConsumer(AsyncWebsocketConsumer):
    events = {}

    @staticmethod
    def to_json(text_data):
        """
        Convert text data as json
        :param text_data:
        :return:
        """
        try:
            data = json.loads(text_data)
            return data
        except TypeError:
            return {"error": {"code": "0004", "message": "Invalid data"}}

    @staticmethod
    def send_error(text_data, error_code=None):
        text_data["error"] = dict() if error_code is None else refer_error(gen_error(error_code))
        return text_data

    def is_auth(self):
        """
        Check user is authenticated or not
        :return: User object if user is authenticated otherwise return None
        """
        try:
            user = self.scope["user"]
            if isinstance(user, AnonymousUser):
                return None
            return user
        except (KeyError, ValueError):
            return None

    async def connect(self):
        await super(AsyncAppWebsocketConsumer, self).connect()

    async def disconnect(self, code):
        await super(AsyncAppWebsocketConsumer, self).disconnect(code)

    async def receive(self, text_data=None, bytes_data=None):
        await super(AsyncAppWebsocketConsumer, self).receive(text_data, bytes_data)

    async def error(self, event=None, code=None, error_data=None):
        CyLog.error(**{"message": "Websocket Error: Event {} - Code: {} - Error data: {}".format(
            event, code, error_data
        )})
        await self.close()
