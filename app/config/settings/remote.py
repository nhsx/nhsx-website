from .base import *  # NOQA

DEBUG = False

ALLOWED_HOSTS = [
    'staging-nhsx.nhs.uk',  # TODO: Update when we know the real staging URL
    'nhsx.nhs.uk'
]

DEFAULT_FILE_STORAGE = 'helpers.storage.MediaRootS3BotoStorage'
AWS_S3_ENDPOINT_URL = ''  # TODO: Update once we know the real endpoint
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
