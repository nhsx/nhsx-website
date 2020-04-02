# -*- coding: utf-8 -*-

"""
    core.models.abstract
    ~~~~~~~~~~~~~~~~~~~~
    Concrete models and mixins for extending page functionality. This code structure helps
    us keep things DRY by creating classes that provide functionality to mutliple page types.

    If you need to add functionality that _every_ page type should get, add it to `BasePage`.
    If you need to add functionality that _some_ page types should get, add a mixin.
    If you need to add functionality that _one_ page type should get, add it to the page model.

"""

from typing import List

# 3rd party
from django.db import models
from django.conf import settings
from wagtail.core import fields
from django.utils.text import slugify
from wagtail.core.models import Page
from wagtail.search import index
from django.utils.translation import ugettext_lazy as _  # NOQA
from wagtail.utils.decorators import cached_classmethod
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import (
    ObjectList, TabbedInterface, StreamFieldPanel, FieldPanel, MultiFieldPanel
)

# Project
from modules.core.blocks import nhsx_blocks


################################################################################
# Mixins
################################################################################


class SocialMetaMixin(models.Model):
    """
        Adds social media meta stuff to the promote tab.

        Twitter summary card image
        Twitter summary card image alt text
        Twitter summary card title
        Twitter summary card description
        FB OG title
        FB OG description
        FB OG image
    """

    class Meta:
        abstract = True

    fb_og_image = models.ForeignKey(
        settings.WAGTAILIMAGES_IMAGE_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text=_('Facebook OG image'),
    )

    fb_og_title = models.CharField(
        max_length=40,
        help_text=_('Facebook OG title - max 40 chars'),
        null=True,
        blank=True
    )

    fb_og_description = models.CharField(
        max_length=300,
        help_text=_('Facebook OG description - max 300 chars'),
        null=True,
        blank=True
    )

    twitter_card_image = models.ForeignKey(
        settings.WAGTAILIMAGES_IMAGE_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text=_('Twitter card image'),
    )

    twitter_card_title = models.CharField(
        max_length=40,
        help_text=_('Twitter card title - max 40 chars'),
        null=True,
        blank=True
    )

    twitter_card_alt_text = models.CharField(
        max_length=100,
        help_text=_('Twitter card image alt text - max 100 chars'),
        null=True,
        blank=True
    )

    twitter_card_description = models.CharField(
        max_length=200,
        help_text=_('Twitter card description - max 200 chars'),
        null=True,
        blank=True
    )

    page_promote_panels = [
        MultiFieldPanel([
            FieldPanel('slug'),
            FieldPanel('seo_title'),
            FieldPanel('search_description'),
        ], heading=_('Common page configuration')),
    ]

    promote_panels = page_promote_panels + [
        MultiFieldPanel([
            ImageChooserPanel('twitter_card_image'),
            FieldPanel('twitter_card_alt_text'),
            FieldPanel('twitter_card_title'),
            FieldPanel('twitter_card_description'),
        ], heading=_("Twitter Meta")),
        MultiFieldPanel([
            ImageChooserPanel('fb_og_image'),
            FieldPanel('fb_og_title'),
            FieldPanel('fb_og_description'),
        ], heading=_("Facebook Meta"))
    ]


class HeroMixin(models.Model):

    """Abstract mixin for use by other Hero mixins.

    Attributes:
        has_hero (bool): Tells the page templates that we have a hero.
    """

    class Meta:
        abstract = True

    has_hero = True


class HeroImageMixin(HeroMixin):

    """A Hero with an Image. Add this to your page class to add a hero with an image.

    Attributes:
        image (models.ForeignKey): Link to the image we want to use
        hero_panels (list): Panels to show for the hero
    """

    class Meta:
        abstract = True

    image = models.ForeignKey(
        settings.WAGTAILIMAGES_IMAGE_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='%(class)s_hero_image'
    )

    hero_panels = [
        ImageChooserPanel('image')
    ]


class HeroContentMixin(HeroMixin):

    class Meta:
        abstract = True

    headline = models.CharField(max_length=255, blank=True, null=True)
    sub_head = models.CharField(max_length=255, blank=True, null=True)

    hero_panels = [
        FieldPanel('headline', classname="title"),
        FieldPanel('sub_head'),
    ]


class HeroImageContentMixin(HeroMixin):

    class Meta:
        abstract = True

    headline = models.CharField(max_length=255, blank=True, null=True)
    sub_head = models.CharField(max_length=255, blank=True, null=True)
    image = models.ForeignKey(
        settings.WAGTAILIMAGES_IMAGE_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='%(class)s_hero_image'
    )

    hero_panels = [
        FieldPanel('headline', classname="title"),
        FieldPanel('sub_head'),
        ImageChooserPanel('image')
    ]


################################################################################
# Base Page
################################################################################


class BasePage(Page, SocialMetaMixin):

    """Make sure any new pages you create extend this one, so that there is a
    centralised place where we can add functionality to all page types.
    """

    class Meta:
        abstract = True

    promote_panels = SocialMetaMixin.promote_panels
    settings_panels = Page.settings_panels

    body = fields.StreamField(
        nhsx_blocks, blank=True, verbose_name="Body blocks"
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('search_description', boost=10),
        index.SearchField('title', boost=5),
        index.SearchField('body')
    ]

    @cached_classmethod
    def get_admin_tabs(cls) -> List[tuple]:
        """Extend the admin tabs in your subclass page by calling this and then
        editing the returned list. Alternatively, leave all of this out of your subclass
        to get the BasePage tabs.

        Example:
            @cached_classmethod
            def get_admin_tabs(cls):
                tabs = super().get_admin_tabs()
                tabs.insert(3, (cls.taxonomy_panels, 'Taxonomy'))
                return tabs

        Returns:
            list: List of tuples
        """
        tabs = [
            (cls.content_panels, 'Content'),
            (cls.promote_panels, 'Promote'),
            (cls.settings_panels, 'Settings'),
        ]
        return tabs

    @cached_classmethod
    def get_edit_handler(cls) -> TabbedInterface:  # NOQA
        """
        """
        tabs = cls.get_admin_tabs()
        edit_handler = TabbedInterface([
            ObjectList(tab[0], heading=tab[1], classname=slugify(tab[1])) for tab in tabs
        ])
        return edit_handler.bind_to(model=cls)


################################################################################
# Base Index Page
################################################################################

class BaseIndexPage(BasePage):

    class Meta:
        abstract = True
