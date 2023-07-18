from .base import *

DEBUG = True
TEST = True
WSGI_APPLICATION = "jooda.wsgi.dev.application"

DATABASES_DEFAULT_NAME = "##############"
DATABASES_DEFAULT_USER = "##############"
DATABASES_DEFAULT_HOST = "##############"
DATABASES_DEFAULT_PASSWORD = "##############"
CACHES_DEFAULT_HOST = "##############"

pymysql.install_as_MySQLdb()
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": DATABASES_DEFAULT_NAME,
        "USER": DATABASES_DEFAULT_USER,
        "PASSWORD": DATABASES_DEFAULT_PASSWORD,
        "HOST": DATABASES_DEFAULT_HOST,
        "PORT": "3306",
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
            "charset": "utf8mb4",
        },
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": CACHES_DEFAULT_HOST,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "SERIALIZER": "django_redis.serializers.json.JSONSerializer",
        },
    },
}


MEDIA_URL = "/tmp/"
