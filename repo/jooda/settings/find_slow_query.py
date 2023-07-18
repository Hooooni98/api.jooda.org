from .dev import *

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "format": {"format": "%(message)s"},
    },
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "slow_query.csv",
            "formatter": "format",
        },
    },
    "loggers": {
        "django.db.backends": {
            "handlers": ["file"],
            "level": "DEBUG",
        },
    },
}
