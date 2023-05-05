import os

from django.core.wsgi import get_wsgi_application


valid_env = ['prod', 'env', 'staging']
env = os.getenv("PROD_ENV")
if env not in valid_env:
    env = 'dev'


setting = "server_config.settings.%s" % env
os.environ.setdefault('DJANGO_SETTINGS_MODULE', setting)

application = get_wsgi_application()
