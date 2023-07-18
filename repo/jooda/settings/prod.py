from .base import *

DEBUG = False
TEST = False
WSGI_APPLICATION = "jooda.wsgi.prod.application"

CSRF_TRUSTED_ORIGINS = ["https://api.jooda.org"]

### ENV ###
AWS_ACCESS_KEY_ID = "##############"
AWS_SECRET_ACCESS_KEY = "##############"
AWS_REGION = "##############"
AWS_STORAGE_BUCKET_NAME = "##############"
DATABASES_DEFAULT_NAME = "##############"
DATABASES_DEFAULT_USER = "##############"
DATABASES_DEFAULT_HOST = "##############"
DATABASES_DEFAULT_PASSWORD = "##############"
CACHES_DEFAULT_HOST = "##############"
JOODA_GUEST_AUTHORIZATION = "##############"

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


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators


# AWS setting
AWS_QUERYSTRING_AUTH = False
# S3 Storages
AWS_S3_CUSTOM_DOMAIN = "%s.s3.%s.amazonaws.com" % (
    AWS_STORAGE_BUCKET_NAME,
    AWS_REGION,
)
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
}
MEDIA_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
S3_CLIENT = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)
