from django.db import models

from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from modelcluster.contrib.taggit import ClusterTaggableManager
from wagtail.admin.edit_handlers import FieldPanel

from modules.core.models.abstract import BasePage, BaseIndexPage

import logging

logger = logging.getLogger(__name__)

class BlogPostIndexPage(BaseIndexPage):
    subpage_types = [ 'BlogPost' ]
    max_count = 1

    def get_context(self, request):
        ctx = super().get_context(request)
        children = BlogPost.objects.live().public().order_by('-first_published_at')

        if request.GET.get('tag', None):
            tags = request.GET.get('tag')
            children = children.filter(tags__slug__in=[tags])

        ctx.update({
            'children': children
        })
        return ctx

class BlogTag(TaggedItemBase):
	content_object = ParentalKey(
	    'BlogPost',
	    related_name='tagged_items',
	    on_delete=models.CASCADE,
	)

class BlogPost(BasePage):
    parent_page_types = ['BlogPostIndexPage']

    tags = ClusterTaggableManager(through=BlogTag, blank=True)

    promote_panels = [
        *BasePage.page_promote_panels,
        FieldPanel("tags"),
        *BasePage.social_promote_panels
    ]
