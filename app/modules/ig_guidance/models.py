from django.db import models
from django import forms
from django.template.response import TemplateResponse
from django.conf import settings
from django.shortcuts import redirect

from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.models import Page
from wagtail import fields
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.images.edit_handlers import FieldPanel
from wagtail.documents.edit_handlers import FieldPanel

from modelcluster.fields import ParentalManyToManyField

from modules.core.models.abstract import BasePage, SluggedCategory
from modules.core.blocks import nhsx_blocks


@register_snippet
class IGGuidanceTopic(SluggedCategory):
    description = models.TextField()

    panels = [
        FieldPanel("name"),
        FieldPanel("description"),
    ]

    class Meta:
        verbose_name = "Information Governance Topic"
        verbose_name_plural = "Information Governance Topics"


@register_snippet
class IGGuidanceTag(SluggedCategory):
    description = models.TextField()

    panels = [
        FieldPanel("name"),
    ]

    class Meta:
        verbose_name = "Information Governance Tag"
        verbose_name_plural = "Information Governance Tags"


class IGGuidance(BasePage):
    subpage_types = ["publications.PublicationPage"]
    topic = models.ForeignKey(
        IGGuidanceTopic, on_delete=models.PROTECT, related_name="+"
    )
    tags = ParentalManyToManyField("IGGuidanceTag", blank=False)
    summary = models.TextField()
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

    content_panels = Page.content_panels + [
        FieldPanel("topic", widget=forms.Select),
        FieldPanel("tags", widget=forms.CheckboxSelectMultiple),
        FieldPanel("summary"),
        FieldPanel("featured_image"),
        FieldPanel("download"),
    ]

    class Meta:
        abstract = True


class InternalGuidance(IGGuidance):
    introduction = fields.StreamField(
        nhsx_blocks, blank=True, verbose_name="Introduction"
    )
    service_user_body = fields.StreamField(
        nhsx_blocks, blank=True, verbose_name="Service User content"
    )
    healthcare_worker_body = fields.StreamField(
        nhsx_blocks, blank=True, verbose_name="Healthcare worker content"
    )
    ig_professional_body = fields.StreamField(
        nhsx_blocks, blank=True, verbose_name="IG professional content"
    )

    content_panels = IGGuidance.content_panels + [
        FieldPanel("introduction"),
        FieldPanel("service_user_body"),
        FieldPanel("healthcare_worker_body"),
        FieldPanel("ig_professional_body"),
    ]

    class Meta:
        verbose_name = "Panel Guidance"


class ExternalGuidance(IGGuidance):
    external_url = models.URLField()

    content_panels = IGGuidance.content_panels + [
        FieldPanel("external_url", widget=forms.URLInput()),
    ]

    def serve(self, request, *args, **kwargs):
        return redirect(self.external_url)

    class Meta:
        verbose_name = "External Guidance"


class IGTemplate(IGGuidance):
    content_panels = IGGuidance.content_panels + [
        FieldPanel("body"),
    ]

    class Meta:
        verbose_name = "Template"


class GuidanceListingPage(RoutablePageMixin, BasePage):
    parent_page_types = ["core.SectionPage"]
    subpage_types = ["InternalGuidance", "ExternalGuidance", "IGTemplate"]

    @route(r"^$")
    @route(r"^tag/([a-z\-0-9]+)/$")
    def filter_by_tag(self, request, tag=None):
        context = self.get_context(request)
        template = self.get_template(request)
        if tag is None:
            guidance = self.get_children().live().specific
        else:
            ids = []
            for klass in self.subpage_types:
                for obj in (
                    eval(klass)
                    .objects.child_of(self)
                    .filter(tags__slug__in=[tag])
                    .live()
                ):
                    ids.append(obj.id)
            guidance = Page.objects.live().filter(id__in=(ids)).specific()

        tags = IGGuidanceTag.objects.all()

        context.update(
            {
                "guidance": guidance,
                "tags": tags,
                "tag": tag,
            }
        )

        return TemplateResponse(request, template, context)
