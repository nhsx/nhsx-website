"""
    documents.models
    ~~~~~~~~~~~~~~~~
    Custom document models.
"""

from django.conf import settings
from django.db import models
from wagtail.documents.models import Document as WagtailDocument, AbstractDocument


class NHSXDocument(AbstractDocument):

    admin_form_fields = WagtailDocument.admin_form_fields


Document = NHSXDocument


################################################################################
# Statistic / Modeladmin models
################################################################################


class DocumentDownload(models.Model):

    document = models.ForeignKey(
        NHSXDocument,
        null=True,
        on_delete=models.SET_NULL,
        related_name="user_downloads",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="document_downloads",
    )
    referrer_path = models.TextField(null=True, blank=True)
    downloaded_at = models.DateTimeField(auto_now_add=True, blank=True)
