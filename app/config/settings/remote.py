import os
from datetime import date, timedelta
from .base import *  # NOQA

DEBUG = False

ALLOWED_HOSTS = ["*"]


####################################################################################################
# AWS
####################################################################################################

THE_FUTURE = date.today() + timedelta(days=365 * 10)

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', None)
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', None)
AWS_HEADERS = {
    'Expires': THE_FUTURE,
    'Cache-Control': 'max-age=86400',
}
AWS_S3_FILE_OVERWRITE = False
AWS_IS_GZIPPED = True
AWS_S3_SECURE_URLS = True
AWS_PRELOAD_METADATA = False


DEFAULT_FILE_STORAGE = 'helpers.storage.MediaRootS3BotoStorage'
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
