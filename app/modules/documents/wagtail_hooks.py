import datetime
import threading
import os

from wagtail.core import hooks
from .models import DocumentDownload
from django.db.models import F


class LogDownload(threading.Thread):
    def __init__(self, document, **kwargs):
        self.document = document
        super(LogDownload, self).__init__(**kwargs)

    def run(self):
        self.document.download_count = F("download_count") + 1
        self.document.save()


@hooks.register("before_serve_document")
def log_document_view(document, request):
    # If we're in test mode, then log the download straight
    # away, otherwise do it in a thread.
    if os.environ.get("PYTEST_CURRENT_TEST"):
        LogDownload(document).run()
    else:
        LogDownload(document).start()
