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
from cacheops import cached  # NOQA
from django.db import models
from django.db.models import F
from django.conf import settings
from wagtail.core import fields
from django.utils.text import slugify
from wagtail.core.models import Page
from wagtail.search import index
from modelcluster.fields import ParentalManyToManyField
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _  # NOQA
from wagtail.utils.decorators import cached_classmethod
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import (
    ObjectList, TabbedInterface, StreamFieldPanel, FieldPanel, MultiFieldPanel
)

# Project
from modules.core.blocks import nhsx_blocks, sidebar_blocks


################################################################################
# Mixins
################################################################################


class SidebarMixin(models.Model):

    """Adds a sidebar to a page containing the content-list component from here:
    https://nhsuk.github.io/nhsuk-frontend/components/contents-list/index.html

    We should attempt to build the list automatically based on sibling pages, but also
    have options to show no sidebar at all, or a curated list of pages.
    """

    class Meta:
        abstract = True

    has_sidebar = True

    automatic = models.BooleanField(
        default=False,
        help_text="Build automatically from sibling pages"
    )

    sidebar_links = fields.StreamField(sidebar_blocks, blank=True)

    panels = [
        FieldPanel('automatic'),
        StreamFieldPanel('sidebar_links')
    ]

    def _find_url(self, val):
        try:
            link = val['link']
            if link['link_page'] is not None:
                return link['link_page'].url
            if link['link_external'] is not None and link['link_external'] != '':
                return link['link_external']
            if link['link_document'] is not None:
                return link['link_document'].url
        except Exception:
            return '/'
        return '/'

    @cached_property
    def _siblings(self):
        sibs = self.get_siblings()
        return [{'title': _.title, 'url': _.url} for _ in sibs]

    @cached_property
    def _streamed(self):
        rv = []
        for item in self.sidebar_links:
            rv.append(
                {
                    'title': item.value.get('label', ""),
                    'url': self._find_url(item.value)
                }
            )

        return rv

    @cached_property
    def sidebar_pages(self):
        if self.automatic:
            return self._siblings
        else:
            return self._streamed


class PageAuthorsMixin(models.Model):
    """
    This class can be used to add authors to a page.
    """
    class Meta:
        abstract = True
    authors = ParentalManyToManyField(
        'users.User',
        blank=True,
        related_name='pages_%(class)s'
    )
    @cached_property
    def author_list(self):
        ordering_model = 'core_articlepage_authors.id'
        authors = self.authors.prefetch_related(
            'profile__photo').order_by(
            ordering_model).annotate(
            avatar_id=F('profile__photo__id')).values_list(
            'first_name', 'last_name', 'slug', 'avatar_id')
        return [
            {
                'full_name': f'{author[0]} {author[1]}',
                'first_name': author[0],
                'last_name': author[1],
                'slug': author[2],
                'avatar': None
            }
            for author in authors
        ]


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

    social_promote_panels = [
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

    promote_panels = page_promote_panels + social_promote_panels


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
