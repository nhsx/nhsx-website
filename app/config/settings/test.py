import os
import logging
from .base import *  # NOQA


DEBUG = True

BASE_URL = "http://0.0.0.0:5000"
COLLECTFAST_ENABLED = False
CACHEOPS_ENABLED = False
WAGTAIL_CACHE = False
ASSETS_DEBUG = True
ASSETS_AUTO_BUILD = True

STATIC_URL = "/static/"
MEDIA_URL = "/media/"

ALLOWED_HOSTS = ["*"]


# Use in-memory SQLite for the tests for speed.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "file::memory:",
    }
}

# Use basic DB search backend for tests
WAGTAILSEARCH_BACKENDS = {
    "default": {
        "BACKEND": "wagtail.search.backends.db",
    },
}

# Override the cache settings so they never interfere with cached keys
# in the site

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "session_cache"
WAGTAIL_CACHE_BACKEND = "wagtail_cache"

REDIS_HOST = os.environ.get("REDIS_HOST", "")
REDIS_PORT = os.environ.get("REDIS_PORT", "6379")
REDIS_HOST_FULL = f"redis://{REDIS_HOST}:{REDIS_PORT}"
REDIS_HOST_CACHEOPS = f"{REDIS_HOST_FULL}/6"
REDIS_HOST_PAGECACHE = f"{REDIS_HOST_FULL}/7"


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_HOST_CACHEOPS,
        "OPTIONS": {
            "PARSER_CLASS": "redis.connection.HiredisParser",
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": os.environ.get("REDIS_PASSWORD"),
            "IGNORE_EXCEPTIONS": True,
        },
    },
    "wagtail_cache": {
        "BACKEND": "wagtailcache.compat_backends.django_redis.RedisCache",
        "LOCATION": REDIS_HOST_PAGECACHE,
        "TIMEOUT": 60 * 60 * 24 * 7,  # Seven days
        "OPTIONS": {
            "PARSER_CLASS": "redis.connection.HiredisParser",
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": os.environ.get("REDIS_PASSWORD"),
            "IGNORE_EXCEPTIONS": True,
        },
    },
    "session_cache": {
        "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
        "LOCATION": os.environ.get("MEMCACHED_LOCATION", "127.0.0.1:11211"),
    },
}


def filter_deprecation_warnings(record):
    warnings_to_suppress = ["RemovedInDjango30Warning"]

    # Return false to suppress message.
    return not any([warn in record.getMessage() for warn in warnings_to_suppress])


warn_logger = logging.getLogger("py.warnings")
warn_logger.addFilter(filter_deprecation_warnings)
