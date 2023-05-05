import logging
from slack_sdk import WebClient

from django.conf import settings


class SlackHandler(logging.Handler):
    def emit(self, record):
        try:
            record.exc_info = record.exc_text = None
            content = {'text': self.format(record)}
            # TODO authorize to thread job
            sc = WebClient(token=settings.TOKEN_AUTH_SLACK, timeout=10)
            sc.chat_postMessage(
                channel="#{}".format(settings.SLACK_API_CHANNEL),
                text="```{}```".format(content['text'])
            )
        except Exception:
            print("Slack handler failed")
