import logging
from .base import *  # NOQA


DEBUG = True

BASE_URL = 'http://0.0.0.0:5000'
COLLECTFAST_ENABLED = False
CACHEOPS_ENABLED = False
WAGTAIL_CACHE = False
ASSETS_DEBUG = True
ASSETS_AUTO_BUILD = True

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

ALLOWED_HOSTS = ['*']


# Use in-memory SQLite for the tests for speed.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'file::memory:',
    }
}

# Use basic DB search backend for tests
WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.search.backends.db',
    },
}


def filter_deprecation_warnings(record):
    warnings_to_suppress = [
        'RemovedInDjango30Warning'
    ]

    # Return false to suppress message.
    return not any([warn in record.getMessage() for warn in warnings_to_suppress])


warn_logger = logging.getLogger('py.warnings')
warn_logger.addFilter(filter_deprecation_warnings)
