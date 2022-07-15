from django.db import models
from django.conf import settings

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel

from modules.core.models.abstract import BasePage
from modules.core.models.abstract import BasePage, BaseIndexPage


class Person(BasePage):
    parent_page_types = ["PeopleListingPage"]
    subpage_types = []

    qualifications = models.CharField(max_length=255, default="", blank=True)
    position = models.CharField(max_length=255, default="", blank=True)

    photo = models.ForeignKey(
        settings.WAGTAILIMAGES_IMAGE_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content_panels = [
        *Page.content_panels,
        FieldPanel("qualifications"),
        FieldPanel("position"),
        ImageChooserPanel("photo"),
        StreamFieldPanel("body"),
    ]

    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "People"


class PeopleListingPage(BaseIndexPage):
    _child_model = Person

    parent_page_types = ["core.SectionPage"]
    subpage_types = ["Person"]

    class Meta:
        verbose_name = "People Listing Page"
        verbose_name_plural = "People Listing Pages"
