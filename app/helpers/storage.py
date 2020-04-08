import os
from tempfile import SpooledTemporaryFile
from django.core.exceptions import SuspiciousOperation

from storages.backends.s3boto3 import S3Boto3Storage
from boto.s3.connection import S3Connection


# By default the S3Connection is using s3.amazonaws.com
# as host, which only allow for S3 hosted in US. To allow
# SEA hosts we need to change the DefaultHost with our own custom
# Connection Class.
class LondonConnection(S3Connection):
    DefaultHost = f"s3-{os.environ.get('AWS_DEFAULT_REGION', 'eu-west-1')}.amazonaws.com"


def safe_join(base, *paths):
    """
    A version of django.utils._os.safe_join for S3 paths.

    Joins one or more path components to the base path component intelligently.
    Returns a normalized version of the final path.

    The final path must be located inside of the base path component (otherwise
    a ValueError is raised).

    Paths outside the base path indicate a possible security sensitive operation.
    """
    from urllib.parse import urljoin
    base_path = base
    paths = map(lambda p: p, paths)
    final_path = urljoin(base_path + ("/" if not base_path.endswith("/") else ""), *paths)
    # Ensure final_path starts with base_path and that the next character after
    # the final path is '/' (or nothing, in which case final_path must be
    # equal to base_path).
    base_path_len = len(base_path) - 1
    if not final_path.startswith(base_path) \
       or final_path[base_path_len:base_path_len + 1] not in ('', '/'):
        raise ValueError('the joined path is located outside of the base path'
                         ' component')
    return final_path


class MediaRootS3BotoStorage(S3Boto3Storage):
    def __init__(self, *args, **kwargs):
        super(MediaRootS3BotoStorage, self).__init__(*args, **kwargs)
        self.connection_class = LondonConnection
        self.location = kwargs.get('location', '')
        self.location = 'media/' + self.location.lstrip('/')
        self.file_overwrite = False

    def _save(self, name, content):
        """
        SEE: https://github.com/jschneier/django-storages/issues/382#issuecomment-592876060

        We create a clone of the content file as when this is passed to
        boto3 it wrongly closes the file upon upload where as the storage
        backend expects it to still be open
        """
        # Seek our content back to the start
        content.seek(0, os.SEEK_SET)

        # Create a temporary file that will write to disk after a specified
        # size. This file will be automatically deleted when closed by
        # boto3 or after exiting the `with` statement if the boto3 is fixed
        with SpooledTemporaryFile() as content_autoclose:

            # Write our original content into our copy that will be closed by boto3
            content_autoclose.write(content.read())

            # Upload the object which will auto close the
            # content_autoclose instance
            return super(MediaRootS3BotoStorage, self)._save(name, content_autoclose)

    def _normalize_name(self, name):
        try:
            return safe_join(self.location, name).lstrip('/')
        except ValueError:
            raise SuspiciousOperation("Attempted access to '%s' denied." % name)
