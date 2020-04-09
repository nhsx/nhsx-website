from django.db import models
from wagtail.core.models import Page
from taggit.models import TaggedItemBase
from modelcluster.fields import ParentalKey
from wagtail.search import index
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel

from modules.core.models.abstract import BasePage, BaseIndexPage, CanonicalMixin
from modelcluster.contrib.taggit import ClusterTaggableManager


class NewsIndexPage(BaseIndexPage):
    subpage_types = ['News']
    max_count = 1


class NewsTags(TaggedItemBase):
    content_object = ParentalKey(
        'news.News',
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_items",
    )


class News(BasePage, CanonicalMixin):
    parent_page_types = ['NewsIndexPage']
    subpage_types = []

    tags = ClusterTaggableManager(through=NewsTags, blank=True)

    settings_panels = CanonicalMixin.panels + BasePage.settings_panels

    search_fields = BasePage.search_fields + [
        index.SearchField('tags', boost=10),
    ]

    content_panels = [
        *Page.content_panels,
        FieldPanel('first_published_at'),
        StreamFieldPanel("body"),
        FieldPanel("tags"),
    ]
