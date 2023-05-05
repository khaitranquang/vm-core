from server_config.settings.dev import *


DEBUG = False
ALLOWED_HOSTS = ["api.staging.onready.net", "api.staging.ready.io"]


CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'shared.channels.app.AppRedisChannelLayer',
        'CONFIG': {
            "hosts": [(os.getenv("CHANNEL_REDIS_STAGING_LOCATION"))],
            "expiry": 2959200           # 3 days
        },
    },
}

DATABASES = {
    'default': {
        'ENGINE': "django.db.backends.mysql",
        'NAME': os.getenv("MYSQL_STAGING_DATABASE"),
        'USER': os.getenv("MYSQL_STAGING_USERNAME"),
        'PASSWORD': os.getenv("MYSQL_STAGING_PASSWORD"),
        'HOST': os.getenv("MYSQL_STAGING_HOST"),
        'PORT': os.getenv("MYSQL_STAGING_PORT"),
        'CONN_MAX_AGE': 300,
        'OPTIONS': {
            'init_command': "ALTER DATABASE `%s` CHARACTER SET utf8mb4; "
                            "SET block_encryption_mode = 'aes-256-cbc'" % (os.getenv("MYSQL_STAGING_DATABASE")),
            'charset': 'utf8mb4',  # <--- Use this,
            'isolation_level': 'read committed'
        }
    }
}


CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.getenv("CACHE_REDIS_STAGING_LOCATION"),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'SOCKET_CONNECT_TIMEOUT': 5,
            'SOCKET_TIMEOUT': 5,
            'IGNORE_EXCEPTIONS': True
        }
    }
}
