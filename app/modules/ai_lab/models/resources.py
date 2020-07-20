from django import forms
from django.db import models
from django.http import Http404
from django.conf import settings

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.documents.edit_handlers import DocumentChooserPanel

from modules.core.models.abstract import BasePage
from modules.core.models.pages import SectionPage, ArticlePage
from modules.blog_posts.models import BlogPost


class AiLabResourceMixin(models.Model):
    parent_page_types = [
        "AiLabUnderstandIndexPage",
        "AiLabDevelopIndexPage",
        "AiLabAdoptIndexPage",
    ]

    summary = models.CharField(max_length=255)
    featured_image = models.ForeignKey(
        settings.WAGTAILIMAGES_IMAGE_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    download = models.ForeignKey(
        settings.WAGTAILDOCS_DOCUMENT_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content_panels = [
        FieldPanel("title"),
        FieldPanel("summary", widget=forms.Textarea),
        ImageChooserPanel("featured_image"),
        DocumentChooserPanel("download"),
        FieldPanel("first_published_at"),
        StreamFieldPanel("body"),
    ]

    def get_template(self, request):
        return "ai_lab/resource.html"

    class Meta:
        abstract = True


class AiLabCaseStudy(AiLabResourceMixin, ArticlePage):
    pass


class AiLabGuidance(AiLabResourceMixin, ArticlePage):
    pass


class AiLabReport(AiLabResourceMixin, ArticlePage):
    pass


class AiLabExternalResource(AiLabResourceMixin, Page):
    external_url = models.URLField()
    content_panels = [
        FieldPanel("title"),
        FieldPanel("summary"),
        ImageChooserPanel("featured_image"),
        FieldPanel("first_published_at"),
        FieldPanel("external_url", widget=forms.URLInput()),
    ]
