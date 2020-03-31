import os
from .remote import *  # NOQA
from .base import MEDIA_ROOT, BASE_DIR  # NOQA

DEBUG = False

BASE_URL = ''  # TODO - Update with a staging URL once we know it

####################################################################################################
# Static assets served by Whitenoise
####################################################################################################


STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'


####################################################################################################
# Media assets served from a CDN / bucket
####################################################################################################


AWS_S3_CUSTOM_DOMAIN = ''  # TODO - add the staging media URL
AWS_STORAGE_BUCKET_NAME = ""  # TODO - add the staging media bucket here
MEDIA_URL = '{}{}/'.format(AWS_S3_CUSTOM_DOMAIN, MEDIA_ROOT)
