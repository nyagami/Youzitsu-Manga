import os

from .base import *


CANONICAL_ROOT_DOMAIN = "youzitsu.ga"

DEBUG = True

ALLOWED_HOSTS = ['youzitsu.ga','127.0.0.1']


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}
