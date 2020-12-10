# stdlib
import logging

# 3rd party
from django.db import models
from wagtail.core import fields
from taggit.models import TagBase, ItemBase
from wagtail.search import index
from dal_select2.widgets import ModelSelect2Multiple
from modelcluster.fields import ParentalKey
from wagtail.core.models import Page
from wagtail.utils.decorators import cached_classmethod
from modelcluster.contrib.taggit import ClusterTaggableManager
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel

# Module
from modules.case_studies.abstract import (
    CaseStudyTag,
    CaseStudyTags,
)

from modules.core.models.abstract import (
    BasePage,
    BaseIndexPage,
    InlineHeroMixin,
    SidebarMixin,
    SubNavMixin,
)

logger = logging.getLogger(__name__)


################################################################################
# Page models
################################################################################


class CaseStudyPage(BasePage, InlineHeroMixin, SidebarMixin):

    display_order = models.IntegerField(default=0, null=False, blank=False,)

    alt_text = models.CharField(max_length=300, null=True, blank=True,)

    tags = ClusterTaggableManager(through=CaseStudyTags, blank=True)

    search_fields = BasePage.search_fields + [
        index.SearchField("tags", boost=10),
    ]

    parent_page_types: list = [
        "core.SectionPage",
    ]

    subpage_types: list = []

    content_panels = [
        *Page.content_panels,
        FieldPanel("display_order"),
        ImageChooserPanel("image"),
        FieldPanel("alt_text"),
        FieldPanel("sub_head"),
        StreamFieldPanel("body"),
        FieldPanel("tags"),
    ]

    sidebar_panels: list = SidebarMixin.panels

    @cached_classmethod
    def get_admin_tabs(cls):
        tabs = super().get_admin_tabs()
        tabs.insert(1, (cls.sidebar_panels, "Sidebar"))
        return tabs
