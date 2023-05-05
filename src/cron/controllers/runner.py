"""
This cron runner implements some cron tasks:
  - store_cached_messages: Store cached messages from redis to ORM Database
"""

from cron.controllers.utils.django_config import django_config
django_config()

import schedule
import time
import traceback
from django.db import close_old_connections

from cron.controllers.utils.logger import Logger


class CronRunner:
    def __init__(self):
        self.logger = Logger()

    def start(self):
        self.logger.info("[+] Starting Ready Chat cron task")
        while True:
            schedule.run_pending()
            time.sleep(1)
