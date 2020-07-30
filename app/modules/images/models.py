# -*- coding: utf-8 -*-

"""
    images.models
    ~~~~~~~~~~~~~
    Custom image models.
"""

from django.db import models
from django.utils.translation import ugettext_lazy as _
from wagtail.images.models import Image, AbstractImage, AbstractRendition


class NHSXImage(AbstractImage):

    caption = models.CharField(
        max_length=255, help_text=_("Image caption"), null=True, blank=True
    )

    credit = models.CharField(
        max_length=255, help_text=_("Image credit"), null=True, blank=True
    )

    alttext = models.CharField(
        max_length=255,
        verbose_name=_("Alt-text"),
        help_text=_("Alt text - good for accesibility"),
        null=True,
        blank=True,
    )

    admin_form_fields = Image.admin_form_fields + ("caption", "credit", "alttext")


class NHSXRendition(AbstractRendition):
    image = models.ForeignKey(
        NHSXImage, on_delete=models.CASCADE, related_name="renditions"
    )

    class Meta:
        unique_together = (("image", "filter_spec", "focal_point_key"),)
