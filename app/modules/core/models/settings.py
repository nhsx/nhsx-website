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
from wagtail.core import blocks, fields
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
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
        verbose_name = 'Analytics settings'

    property_id = models.CharField(
        help_text='Property ID',
        null=True,
        blank=True,
        max_length=32)


@register_setting
class SocialMediaSettings(CachedSetting):

    class Meta:
        verbose_name = 'Social media accounts'

    facebook = models.URLField(
        help_text='Your Facebook page URL',
        null=True,
        blank=True)
    facebook_app_id = models.URLField(
        help_text='Your Facebook app ID if you have one',
        null=True,
        blank=True)
    instagram = models.CharField(
        max_length=255, help_text='Your Instagram url',
        null=True,
        blank=True)
    twitter = models.CharField(
        max_length=255, help_text='Your Twitter url',
        null=True,
        blank=True)
    youtube = models.CharField(
        max_length=255, help_text='Your YouTube url',
        null=True,
        blank=True)


@register_setting
class MetaTagSettings(CachedSetting):

    class Meta:
        verbose_name = 'Meta and social sharing tags'

    description = models.TextField(
        help_text="Fallback description if there isn't one set on the page",
        null=True,
        blank=True)

    image = models.ForeignKey(
        settings.WAGTAILIMAGES_IMAGE_MODEL,
        help_text='A fallback image to use when shared on Facebook and Twitter (aim for 1200x630)',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+')

    panels = [
        FieldPanel('description'),
        ImageChooserPanel('image')
    ]


@register_setting
class DefaultImageSettings(CachedSetting):

    class Meta:
        verbose_name = 'Default / fallback image settings'

    image = models.ForeignKey(
        settings.WAGTAILIMAGES_IMAGE_MODEL,
        help_text='A default image to use when none is present for a page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+')

    panels = [
        ImageChooserPanel('image')
    ]
