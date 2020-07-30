# stdlib
import logging

# 3rd party
from django.db import models
from wagtail.core import fields
from taggit.models import TaggedItemBase
from wagtail.search import index
from dal_select2.widgets import ModelSelect2Multiple
from modelcluster.fields import ParentalKey
from wagtail.core.models import Page
from wagtail.utils.decorators import cached_classmethod
from modelcluster.contrib.taggit import ClusterTaggableManager
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel

# Project
from modules.core.blocks import blog_link_blocks
from modules.core.models.abstract import (
    BasePage,
    BaseIndexPage,
    CanonicalMixin,
    PageAuthorsMixin,
)


logger = logging.getLogger(__name__)


class BlogTags(TaggedItemBase):
    content_object = ParentalKey(
        "blog_posts.BlogPost",
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_items",
    )


class FeaturedBlogsMixin(models.Model):
    class Meta:
        abstract = True

    featured_posts = fields.StreamField(blog_link_blocks, blank=True)

    panels = [StreamFieldPanel("featured_posts")]


################################################################################
# Page models
################################################################################


class BlogPost(BasePage, PageAuthorsMixin, CanonicalMixin):
    parent_page_types = ["BlogPostIndexPage"]
    subpage_types = []

    tags = ClusterTaggableManager(through=BlogTags, blank=True)

    search_fields = BasePage.search_fields + [
        index.SearchField("tags", boost=10),
    ]

    content_panels = [
        *Page.content_panels,
        FieldPanel("first_published_at"),
        FieldPanel("authors", widget=ModelSelect2Multiple(url="author-autocomplete")),
        StreamFieldPanel("body"),
        FieldPanel("tags"),
    ]

    settings_panels = CanonicalMixin.panels + BasePage.settings_panels


class BlogPostIndexPage(BaseIndexPage, FeaturedBlogsMixin):

    _child_model = BlogPost

    subpage_types = ["BlogPost"]
    max_count = 1

    @cached_classmethod
    def get_admin_tabs(cls):
        tabs = super().get_admin_tabs()
        tabs.insert(1, (FeaturedBlogsMixin.panels, "Featured"))
        return tabs
