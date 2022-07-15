import random

from django import forms
from django.db import models
from django.http import Http404
from django.conf import settings
from django.utils.text import slugify
from django.shortcuts import redirect

from wagtail.admin.panels import FieldPanel, FieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.models import Page
from wagtail import fields
from wagtail.images.edit_handlers import FieldPanel
from wagtail.documents.edit_handlers import FieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.utils.decorators import cached_classmethod

from modelcluster.fields import ParentalManyToManyField

from modules.core.models.abstract import BasePage, SluggedCategory
from modules.core.models.pages import SectionPage, ArticlePage
from modules.blog_posts.models import BlogPost
from modules.ai_lab.blocks import resource_link_blocks


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

    topics = ParentalManyToManyField("AiLabTopic", blank=False)
    featured_resources = fields.StreamField(resource_link_blocks, blank=True)

    content_panels = [
        FieldPanel("title"),
        FieldPanel("summary", widget=forms.Textarea),
        FieldPanel("featured_image"),
        FieldPanel("download"),
        FieldPanel("first_published_at"),
        FieldPanel("topics", widget=forms.CheckboxSelectMultiple),
        FieldPanel("body"),
    ]

    @cached_classmethod
    def get_admin_tabs(cls):
        tabs = super().get_admin_tabs()
        del tabs[1]
        tabs.insert(1, ([FieldPanel("featured_resources")], "Featured"))
        return tabs

    def get_template(self, request):
        return "ai_lab/resource.html"

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        topics = self.topics.all()

        if len(self.featured_resources) == 0:
            context["featured_resources"] = self._get_featured_resources(topics)
        else:
            context["featured_resources"] = [
                resource.value for resource in self.featured_resources
            ]
        return context

    def _get_featured_resources(self, topics):
        from modules.ai_lab.models import AiLabResourceIndexPage

        root_page = AiLabResourceIndexPage.objects.all()[0]

        child_resources = list(root_page._get_resources().live())

        if self in child_resources:
            child_resources.remove(self)

        featured_resources = []

        # Try and find resources with the same topic(s) first
        if len(child_resources) > 0:
            for resource in child_resources:
                if len(featured_resources) == 3:
                    break
                for topic in topics:
                    if topic in resource.topics.all():
                        if resource not in featured_resources:
                            featured_resources.append(resource)

            # If there are not enough resources with a topic, then pad
            # the remainder with random resource(s)
            if len(featured_resources) < 3:
                remainder = 3 - len(featured_resources)
                if len(child_resources) >= remainder:
                    featured_resources.extend(random.sample(child_resources, remainder))

        return featured_resources

    class Meta:
        abstract = True


@register_snippet
class AiLabTopic(SluggedCategory):
    class Meta:
        verbose_name = "AI Lab Topic"
        verbose_name_plural = "AI Lab Topics"


class AiLabCaseStudy(AiLabResourceMixin, ArticlePage):
    subpage_types = ["publications.PublicationPage"]

    class Meta:
        verbose_name = "Case Study"
        verbose_name_plural = "Case Studies"


class AiLabGuidance(AiLabResourceMixin, ArticlePage):
    subpage_types = ["publications.PublicationPage"]

    class Meta:
        verbose_name = "Guidance"
        verbose_name_plural = "Guidance"


class AiLabReport(AiLabResourceMixin, ArticlePage):
    subpage_types = ["publications.PublicationPage"]

    class Meta:
        verbose_name = "Report"
        verbose_name_plural = "Reports"


class AiLabLinkedResourceMixin(AiLabResourceMixin):
    content_panels = [
        FieldPanel("title"),
        FieldPanel("summary", widget=forms.Textarea),
        FieldPanel("featured_image"),
        FieldPanel("first_published_at"),
        FieldPanel("topics", widget=forms.CheckboxSelectMultiple),
    ]

    def serve(self, request, *args, **kwargs):
        return redirect(self.resource_url())

    class Meta:
        abstract = True


class AiLabExternalResource(AiLabLinkedResourceMixin, Page):
    external_url = models.URLField()
    content_panels = AiLabLinkedResourceMixin.content_panels + [
        FieldPanel("external_url", widget=forms.URLInput())
    ]

    def resource_url(self):
        return self.external_url

    class Meta:
        verbose_name = "External Resource"
        verbose_name_plural = "External Resources"


class AiLabInternalResource(AiLabLinkedResourceMixin, Page):
    page = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    content_panels = AiLabLinkedResourceMixin.content_panels + [FieldPanel("page")]

    def resource_url(self):
        return self.page.url

    class Meta:
        verbose_name = "Internal Resource"
        verbose_name_plural = "Internal Resources"
