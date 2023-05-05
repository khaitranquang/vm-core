import os
from pathlib import Path
import dotenv
import traceback

import django

from cron.controllers.utils.logger import logger


def django_config():
    try:
        valid_env = ['prod', 'env', 'staging']
        env = os.getenv("PROD_ENV")
        if env not in valid_env:
            env = 'dev'
        if env == 'dev':
            env_file = os.path.join(Path(__file__).resolve().parent.parent.parent.parent, '.env')
            dotenv.read_dotenv(env_file)

        setting = "server_config.settings.%s" % env
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", setting)
        django.setup()
    except:
        tb = traceback.format_exc()
        logger.error(tb)
