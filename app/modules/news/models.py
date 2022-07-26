# 3rd party
from django.db import models
from wagtail import fields
from taggit.models import TaggedItemBase
from wagtail.search import index
from modelcluster.fields import ParentalKey
from wagtail.models import Page
from wagtail.utils.decorators import cached_classmethod
from modelcluster.contrib.taggit import ClusterTaggableManager
from wagtail.admin.panels import FieldPanel, StreamFieldPanel

# Project
from modules.core.blocks import news_link_blocks
from modules.core.models.abstract import BasePage, BaseIndexPage, CanonicalMixin


class FeaturedNewsMixin(models.Model):
    class Meta:
        abstract = True

    featured_posts = fields.StreamField(news_link_blocks, blank=True)

    panels = [StreamFieldPanel("featured_posts")]


class NewsTags(TaggedItemBase):
    content_object = ParentalKey(
        "news.News",
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_items",
    )


################################################################################
# Page models
################################################################################


class News(BasePage, CanonicalMixin):
    parent_page_types = ["NewsIndexPage"]
    subpage_types = []

    tags = ClusterTaggableManager(through=NewsTags, blank=True)

    settings_panels = CanonicalMixin.panels + BasePage.settings_panels

    search_fields = BasePage.search_fields + [
        index.SearchField("tags", boost=10),
    ]

    content_panels = [
        *Page.content_panels,
        FieldPanel("first_published_at"),
        StreamFieldPanel("body"),
        FieldPanel("tags"),
    ]


class NewsIndexPage(BaseIndexPage, FeaturedNewsMixin):

    _child_model = News

    subpage_types = ["News"]
    max_count = 1

    @cached_classmethod
    def get_admin_tabs(cls):
        tabs = super().get_admin_tabs()
        tabs.insert(1, (FeaturedNewsMixin.panels, "Featured"))
        return tabs
