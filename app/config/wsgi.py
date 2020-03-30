"""
WSGI config.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""
import os

# Try to import envkey, otherwise trust that the environment variables
# are being injected another way
try:
    import envkey  # NOQA
except Exception:
    pass

from django.core.wsgi import get_wsgi_application

server_env = os.environ.get("SERVER_ENV", '')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.{}".format(server_env))
os.environ.setdefault("BUGSNAG_RELEASE_STAGE", server_env)

application = get_wsgi_application()
