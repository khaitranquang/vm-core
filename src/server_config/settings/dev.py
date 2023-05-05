import os
import traceback
from pathlib import Path
import logging.config


BASE_DIR = Path(__file__).resolve().parent.parent

try:
    SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
    DEBUG = True
    ALLOWED_HOSTS = ["*"]
    WSGI_APPLICATION = 'server_config.wsgi.application'
    ASGI_APPLICATION = 'server_config.routing.application'

    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'shared.channels.app.AppRedisChannelLayer',
            'CONFIG': {
                "hosts": [(os.getenv("CHANNEL_REDIS_LOCATION"))],
            },
        },
    }

    # Database
    DATABASES = {
        'default': {
            'ENGINE': "django_prometheus.db.backends.mysql",
            'NAME': os.getenv("MYSQL_DATABASE"),
            'USER': os.getenv("MYSQL_USERNAME"),
            'PASSWORD': os.getenv("MYSQL_PASSWORD"),
            'HOST': os.getenv("MYSQL_HOST"),
            'PORT': os.getenv("MYSQL_PORT"),
            'CONN_MAX_AGE': 300,
            'OPTIONS': {
                'init_command': "ALTER DATABASE `%s` CHARACTER SET utf8mb4; "
                                "SET block_encryption_mode = 'aes-256-cbc'" % (os.getenv("MYSQL_DATABASE")),
                'charset': 'utf8mb4',  # <--- Use this,
                'isolation_level': 'read committed'
            }
        }
    }

    # Cache db
    CACHES = {
        'default': {
            'BACKEND': 'django_prometheus.cache.backends.redis.RedisCache',
            'LOCATION': os.getenv("CACHE_REDIS_LOCATION"),
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
                'SOCKET_CONNECT_TIMEOUT': 5,
                'SOCKET_TIMEOUT': 5,
                'IGNORE_EXCEPTIONS': True
            }
        }
    }
    DJANGO_REDIS_IGNORE_EXCEPTIONS = True

    # Application definition
    INSTALLED_APPS = [
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.staticfiles',
        'corsheaders',
        'rest_framework',
        'channels',
        'django_prometheus',
        'api_orm',
        'api'
    ]

    AUTHENTICATION_BACKENDS = [
        'django.contrib.auth.backends.AllowAllUsersModelBackend'
    ]

    MIDDLEWARE = [
        'django_prometheus.middleware.PrometheusBeforeMiddleware',
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'corsheaders.middleware.CorsPostCsrfMiddleware',
        'shared.middlewares.queries_debug_middleware.QueriesDebugMiddleware',
        'shared.middlewares.error_response_middleware.ErrorResponseMiddleware',
        'django_prometheus.middleware.PrometheusAfterMiddleware',
    ]

    ROOT_URLCONF = 'server_config.urls'

    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'shared.authentications.app.AppGeneralAuthentication'
        ],
        'DEFAULT_PERMISSION_CLASSES': (
            'shared.permissions.app.AppBasePermission',
        ),
        'DEFAULT_RENDERER_CLASSES': ('rest_framework.renderers.JSONRenderer',),
        'EXCEPTION_HANDLER': 'shared.exception_handler.custom_exception_handler',
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
        'PAGE_SIZE': 10,
        'DEFAULT_THROTTLE_CLASSES': (
            'shared.throttling.app.AppBaseThrottle'
        ),
        'DEFAULT_THROTTLE_RATES': {
            'anonymous': '60/min',
            'user_authenticated': '600/min',
            'users.auth': '20/hour',
            'users.update': '10/min',
        }
    }

    # -------------------------- 3rd Libraries ------------------------------ #
    # Token auth slack (Logging)
    TOKEN_AUTH_SLACK = os.getenv("TOKEN_AUTH_SLACK")
    SLACK_API_CHANNEL = os.getenv("SLACK_API_CHANNEL")
    SLACK_CRON_CHANNEL = os.getenv("SLACK_CRON_CHANNEL")

    # FCM Token
    FCM_CRED_SERVICE_ACCOUNT = os.getenv("FCM_CRED_SERVICE_ACCOUNT")

    # AWS Storage
    AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME")
    AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET")
    AWS_S3_ACCESS_KEY = os.getenv("AWS_S3_ACCESS_KEY")
    AWS_S3_SECRET_KEY = os.getenv("AWS_S3_SECRET_KEY")
    AWS_CLOUDFRONT_PRIVATE_KEY_PEM = os.getenv("AWS_CLOUDFRONT_PRIVATE_KEY_PEM")
    AWS_CLOUDFRONT_PUBLIC_KEY_ID = os.getenv("AWS_CLOUDFRONT_PUBLIC_KEY_ID")

    # DigitalOcean Spaces Storage
    DO_SPACES_ENDPOINT_URL = os.getenv("DO_SPACES_ENDPOINT_URL")
    DO_SPACES_REGION_NAME = os.getenv("DO_SPACES_REGION_NAME")
    DO_SPACES_BUCKET = os.getenv("DO_SPACES_BUCKET")
    DO_SPACES_ACCESS_KEY = os.getenv("DO_SPACES_ACCESS_KEY")
    DO_SPACES_SECRET_KEY = os.getenv("DO_SPACES_SECRET_KEY")
    DO_CDN_PRIVATE_KEY = os.getenv("DO_CDN_PRIVATE_KEY")
    DO_CDN_PUBLIC_KEY = os.getenv("DO_CDN_PUBLIC_KEY")
    DO_SPACES_SUB_URL = os.getenv("DO_SPACES_SUB_URL")

    # Management commands secret token
    MANAGEMENT_COMMAND_TOKEN = os.getenv("MANAGEMENT_COMMAND_TOKEN")

    # CORS Config
    CORS_ORIGIN_ALLOW_ALL = False
    CORS_ORIGIN_REGEX_WHITELIST = []
    CORS_ALLOW_CREDENTIALS = True
    CORS_EXPOSE_HEADERS = (
        'location',
        'Location',
        'device-id',
        'Device-Id',
        'device-expired-time',
        'Device-Expired-Time'
    )
    CORS_ALLOW_HEADERS = (
        'accept',
        'accept-encoding',
        'authorization',
        'content-type',
        'dnt',
        'origin',
        'user-agent',
        'x-csrftoken',
        'x-requested-with',
        'device-id',
        'device-expired-time',
    )
    CORS_ALLOW_METHODS = (
        'GET',
        'POST',
        'PUT',
        'DELETE',
        'OPTIONS'
    )

    # Internationalization
    LANGUAGE_CODE = 'en-us'
    TIME_ZONE = 'UTC'
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    STATIC_URL = '/static/'

    # Default primary key field type
    # https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

except Exception as e:
    from shared.log.config import logging_config
    logging.config.dictConfig(logging_config)
    logger = logging.getLogger('slack_service')
    tb = traceback.format_exc()
    logger.critical(tb)
