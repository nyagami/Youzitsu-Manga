import os

from .base import *


CANONICAL_ROOT_DOMAIN = "youzitsu.ga"

DEBUG = True

ALLOWED_HOSTS = ['youzitsu.ga','127.0.0.1','localhost']


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}