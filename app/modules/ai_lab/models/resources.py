from django import forms
from django.db import models
from django.http import Http404

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.models import Page

from modules.core.models.abstract import BasePage
from modules.core.models.pages import SectionPage, ArticlePage
from modules.blog_posts.models import BlogPost


class AiLabResourceMixin(models.Model):
    parent_page_types = [
        "AiLabUnderstandIndexPage",
        "AiLabDevelopIndexPage",
        "AiLabAdoptIndexPage",
    ]

    class Meta:
        abstract = True


class AiLabCaseStudy(AiLabResourceMixin, ArticlePage):
    pass


class AiLabExternalResource(AiLabResourceMixin, Page):
    external_url = models.URLField()
    content_panels = Page.content_panels + [
        FieldPanel("external_url", widget=forms.URLInput()),
    ]
