from django.db import models

from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from modelcluster.contrib.taggit import ClusterTaggableManager
from wagtail.admin.edit_handlers import FieldPanel

from modules.core.models.abstract import BasePage, BaseIndexPage

class BlogPostIndexPage(BaseIndexPage):
    subpage_types = [ 'BlogPost' ]
    max_count = 1

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
