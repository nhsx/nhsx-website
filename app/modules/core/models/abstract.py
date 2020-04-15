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
from modelcluster.fields import ParentalManyToManyField, ParentalKey
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _  # NOQA
from wagtail.utils.decorators import cached_classmethod
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import (
    ObjectList, TabbedInterface, StreamFieldPanel, FieldPanel, MultiFieldPanel
)
from taggit.models import TaggedItemBase

# Project
from modules.core.blocks import nhsx_blocks, page_link_blocks


################################################################################
# Mixins
################################################################################


class CanonicalMixin(models.Model):

    class Meta:
        abstract = True

    canonical_rel = models.URLField(
        "Canonical link",
        null=True,
        blank=True,
        help_text="If this article was first published elsewhere, put that link here to help SEO"
    )

    panels = [
        FieldPanel('canonical_rel'),
    ]


class PageLinksMixin(models.Model):
    class Meta:
        abstract = True

    sidebar_title = models.CharField(
        "Title",
        max_length=255,
        blank=True,
        null=True,
        default="Related Pages",
        help_text="The title to appear above the links in the sidebar"
    )
    page_links = fields.StreamField(page_link_blocks, blank=True)

    panels = [
        FieldPanel('sidebar_title'),
        FieldPanel('automatic'),
        StreamFieldPanel('page_links')
    ]

    automatic = models.BooleanField(
        default=False,
        help_text="Build automatically from sibling pages"
    )

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
    def _streamed(self):
        rv = []
        for item in self.page_links:
            rv.append(
                {
                    'title': item.value.get('label', ""),
                    'url': self._find_url(item.value)
                }
            )

        return rv


class SubNavMixin(PageLinksMixin):
    class Meta:
        abstract = True

    automatic = models.BooleanField(
        default=False,
        help_text="Build automatically from child pages"
    )

    @cached_property
    def _children(self):
        children = self.get_children()
        return [{'title': _.title, 'url': _.url} for _ in children]

    @cached_property
    def subnav_pages(self):
        if self.automatic:
            return self._children
        else:
            return self._streamed


class SidebarMixin(PageLinksMixin):

    """Adds a sidebar to a page containing the content-list component from here:
    https://nhsuk.github.io/nhsuk-frontend/components/contents-list/index.html

    We should attempt to build the list automatically based on sibling pages, but also
    have options to show no sidebar at all, or a curated list of pages.
    """
    class Meta:
        abstract = True

    has_sidebar = True

    @cached_property
    def _siblings(self):
        sibs = self.get_siblings()
        return [{'title': _.title, 'url': _.url} for _ in sibs]

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
        blank=False,
        related_name='pages_%(class)s'
    )

    @cached_property
    def author_list(self):
        from modules.images.service import _images
        authors = self.authors.prefetch_related(
            'profile__photo').annotate(
            avatar_id=F('profile__photo__id')).values_list(
            'first_name', 'last_name', 'slug', 'avatar_id', 'profile__job_title')
        return [
            {
                'full_name': f'{author[0]} {author[1]}',
                'first_name': author[0],
                'last_name': author[1],
                'slug': author[2],
                'avatar': _images.first(id=author[3]),
                'job_title': author[4]
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

    extra_search_fields = [
        index.SearchField('headline'),
        index.SearchField('sub_head'),
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

    extra_search_fields = [
        index.SearchField('headline'),
        index.SearchField('sub_head'),
    ]


class InlineHeroMixin(HeroMixin):

    class Meta:
        abstract = True

    sub_head = models.CharField(max_length=255, blank=True, null=True)
    image = models.ForeignKey(
        settings.WAGTAILIMAGES_IMAGE_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='%(class)s_hero_image'
    )

    extra_search_fields = [
        index.SearchField('sub_head'),
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

class BaseIndexPage(BasePage, InlineHeroMixin):

    class Meta:
        abstract = True

    search_fields = BasePage.search_fields + InlineHeroMixin.extra_search_fields

    content_panels = [
        *Page.content_panels,
        FieldPanel("sub_head"),
        ImageChooserPanel("image"),
        StreamFieldPanel("body"),
    ]

    @cached_classmethod
    def get_admin_tabs(cls):
        tabs = super().get_admin_tabs()
        return tabs
