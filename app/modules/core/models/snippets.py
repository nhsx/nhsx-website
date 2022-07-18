# 3rd party
from django import forms

from wagtail import blocks
from django.db import models
from wagtail.snippets.models import register_snippet
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel


################################################################################
# Legal Snippets
################################################################################


@register_snippet
class LegalInformation(models.Model):

    name = models.CharField(max_length=100)
    body = RichTextField(blank=True)

    panels = [
        FieldPanel("name"),
        FieldPanel("body", classname="full"),
    ]

    class Meta:
        verbose_name = "Legal Information"
        verbose_name_plural = "Legal Information"

    def __str__(self):
        return self.name
