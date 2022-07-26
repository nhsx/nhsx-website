# -*- coding: utf-8 -*-

"""
    core.models.settings
    ~~~~~~~~~~~~~~~~~~~~
    Stuff that goes in the settings.
"""

from __future__ import absolute_import, unicode_literals

# 3rd party
from cacheops import cached  # NOQA
from django.db import models
from django.conf import settings
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.models import Orderable
from wagtail.admin.panels import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    FieldPanel,
)
from wagtail.images.edit_handlers import FieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting


################################################################################
# Settings models
################################################################################


class CachedSetting(BaseSetting):
    class Meta:
        abstract = True

    @classmethod
    # @cached(timeout=60 * 60 * 24)
    def for_site(cls, site):
        """
        Get an instance of this setting for the site.
        """
        instance, created = cls.objects.get_or_create(site=site)
        return instance


@register_setting
class AnalyticsSettings(CachedSetting):
    class Meta:
        verbose_name = "Analytics settings"

    property_id = models.CharField(
        help_text="Property ID", null=True, blank=True, max_length=32
    )


@register_setting
class SocialMediaSettings(CachedSetting):
    class Meta:
        verbose_name = "Social media accounts"

    facebook = models.URLField(
        help_text="Your Facebook page URL", null=True, blank=True
    )
    facebook_app_id = models.URLField(
        help_text="Your Facebook app ID if you have one", null=True, blank=True
    )
    instagram = models.CharField(
        max_length=255, help_text="Your Instagram url", null=True, blank=True
    )
    twitter = models.CharField(
        max_length=255,
        help_text='Your Twitter username (without the @ symbol, for example "NHSX")',
        null=True,
        blank=True,
    )
    youtube = models.CharField(
        max_length=255, help_text="Your YouTube url", null=True, blank=True
    )

    site_name = models.CharField(
        max_length=255,
        help_text="The name of the website which will be associated with some social media shares",
        null=True,
        blank=True,
    )


@register_setting
class MetaTagSettings(CachedSetting):
    class Meta:
        verbose_name = "Meta and social sharing tags"

    description = models.TextField(
        help_text="Fallback description if there isn't one set on the page",
        null=True,
        blank=True,
    )

    image = models.ForeignKey(
        settings.WAGTAILIMAGES_IMAGE_MODEL,
        help_text="A fallback image to use when shared on Facebook and Twitter (aim for 1200x630)",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [FieldPanel("description"), FieldPanel("image")]


@register_setting
class DefaultImageSettings(CachedSetting):
    class Meta:
        verbose_name = "Default / fallback image settings"

    image = models.ForeignKey(
        settings.WAGTAILIMAGES_IMAGE_MODEL,
        help_text="A default image to use when none is present for a page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [FieldPanel("image")]


@register_setting
class HeaderSettings(ClusterableModel, BaseSetting):
    service_name = models.CharField(max_length=255, blank=True)
    service_long_name = models.BooleanField(default=False)
    service_link = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="service_link",
    )

    transactional = models.BooleanField(default=False)

    logo_link = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    logo_aria = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Aria label override for the NHS logo.",
    )

    show_search = models.BooleanField(default=False)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("service_name"),
                FieldPanel("service_long_name"),
                FieldPanel("service_link"),
                FieldPanel("transactional"),
            ],
            heading="Service",
        ),
        MultiFieldPanel(
            [
                FieldPanel("logo_link"),
                FieldPanel("logo_aria"),
            ],
            heading="Logo",
        ),
        FieldPanel("show_search"),
        InlinePanel("navigation_links", heading="Navigation"),
    ]


class AbstractLink(Orderable):
    class Meta:
        abstract = True
        ordering = ["sort_order"]

    label = models.CharField(max_length=255)
    page = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [
        FieldPanel("label"),
        FieldPanel("page"),
    ]


class NavigationLink(AbstractLink):
    setting = ParentalKey(
        HeaderSettings,
        on_delete=models.CASCADE,
        related_name="navigation_links",
    )


@register_setting
class FooterSettings(ClusterableModel, BaseSetting):

    fixed_coloumn_footer = models.BooleanField(
        "Fixed column footer",
        default=False,
        help_text="""Enable this setting to change way the footer is styled,
        so links group into columns""",
    )

    panels = [
        FieldPanel("fixed_coloumn_footer"),
        InlinePanel(
            "footer_links",
            label="Footer Links",
            help_text="There is a minimum of 1 link and a maximum of 9 ",
            min_num=1,
            max_num=9,
        ),
    ]


class FooterLinks(AbstractLink):

    setting = ParentalKey(
        FooterSettings,
        on_delete=models.CASCADE,
        related_name="footer_links",
    )
