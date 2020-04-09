from django.db import models

from dal_select2.widgets import ModelSelect2Multiple
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from modelcluster.contrib.taggit import ClusterTaggableManager
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.models import Page
from wagtail.search import index

from modules.core.models.abstract import (
    BasePage, BaseIndexPage, PageAuthorsMixin, CanonicalMixin
)

import logging

logger = logging.getLogger(__name__)


class BlogPostIndexPage(BaseIndexPage):
    subpage_types = ['BlogPost']
    max_count = 1

    def get_context(self, request):
        ctx = super().get_context(request)
        children = BlogPost.objects.live().public().order_by('-first_published_at')

        if request.GET.get('tag', None):
            tags = request.GET.get('tag').split(',')
            children = children.filter(tags__slug__in=tags).distinct()

        ctx.update({
            'children': children
        })
        return ctx


class BlogTags(TaggedItemBase):
    content_object = ParentalKey(
        'blog_posts.BlogPost',
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_items",
    )


class BlogPost(BasePage, PageAuthorsMixin, CanonicalMixin):
    parent_page_types = ['BlogPostIndexPage']
    subpage_types = []

    tags = ClusterTaggableManager(through=BlogTags, blank=True)

    search_fields = BasePage.search_fields + [
        index.SearchField('tags', boost=10),
    ]

    content_panels = [
        *Page.content_panels,
        FieldPanel('first_published_at'),
        FieldPanel(
            'authors',
            widget=ModelSelect2Multiple(url='author-autocomplete')
        ),
        StreamFieldPanel("body"),
        FieldPanel("tags"),
    ]

    settings_panels = CanonicalMixin.panels + BasePage.settings_panels
