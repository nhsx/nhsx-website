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
from modules.core.models.abstract import (
    BasePage,
    BaseIndexPage,
    CanonicalMixin,
    PageAuthorsMixin,
)


logger = logging.getLogger(__name__)


################################################################################
# Page models
################################################################################


class LongformPost(BasePage, PageAuthorsMixin, CanonicalMixin):
    parent_page_types = ["LongformPostIndexPage"]
    subpage_types = []

    content_panels = [
        *Page.content_panels,
        FieldPanel("first_published_at"),
        FieldPanel("authors", widget=ModelSelect2Multiple(url="author-autocomplete")),
        StreamFieldPanel("body"),
        # FieldPanel("tags"),
    ]

    settings_panels = CanonicalMixin.panels + BasePage.settings_panels


class LongformPostIndexPage(BaseIndexPage):

    _child_model = LongformPost

    subpage_types = ["LongformPost"]
    max_count = 1
