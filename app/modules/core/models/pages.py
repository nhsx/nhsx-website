# 3rd party
from wagtail.core import fields
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.utils.decorators import cached_classmethod

# Project
from modules.core.blocks import nhsx_blocks

# Module
from .abstract import BasePage, HeroImageContentMixin, SidebarMixin, SubNavMixin


################################################################################
# SectionPage
################################################################################


class SectionPage(BasePage, HeroImageContentMixin, SubNavMixin):

    """SectionPage is a top level page for containing grouped articles.

    """

    parent_page_types: list = ['home.HomePage', 'core.SectionPage', ]
    subpage_types: list = ['core.ArticlePage', 'core.SectionPage', ]

    hero_panels: list = HeroImageContentMixin.hero_panels
    subnav_panels: list = SubNavMixin.panels

    search_fields = BasePage.search_fields + HeroImageContentMixin.extra_search_fields

    @cached_classmethod
    def get_admin_tabs(cls):
        tabs = super().get_admin_tabs()
        tabs.insert(1, (cls.hero_panels, 'Hero'))
        tabs.insert(2, (cls.subnav_panels, 'Subnavigation'))
        return tabs

    def subnav_items_per_row(self):
        if (len(self.subnav_pages) % 3 == 0):
            return 3
        else:
            return 2

    def subnav_column_class(self):
        if (len(self.subnav_pages) % 3 == 0):
           return  "one-third"
        else:
            return "one-half"


################################################################################
# ArticlePage
################################################################################


class ArticlePage(BasePage, SidebarMixin):

    """ArticlePage is a generic content page.

    """

    parent_page_types: list = ['core.SectionPage', 'home.HomePage']
    subpage_types: list = []

    sidebar_panels: list = SidebarMixin.panels

    @cached_classmethod
    def get_admin_tabs(cls):
        tabs = super().get_admin_tabs()
        tabs.insert(1, (cls.sidebar_panels, 'Sidebar'))
        return tabs
