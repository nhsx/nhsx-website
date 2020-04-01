# 3rd party
from wagtail.core import fields
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.utils.decorators import cached_classmethod

# Project
from modules.core.blocks import nhsx_blocks

# Module
from .abstract import BasePage, HeroImageContentMixin


################################################################################
# SectionPage
################################################################################


class SectionPage(BasePage, HeroImageContentMixin):

    """SectionPage is a top level page for containing grouped articles.

    """

    parent_page_types: list = ['home.HomePage', ]
    subpage_types: list = ['core.ArticlePage', ]

    hero_panels: list = HeroImageContentMixin.hero_panels

    @cached_classmethod
    def get_admin_tabs(cls):
        tabs = super().get_admin_tabs()
        tabs.insert(1, (cls.hero_panels, 'Hero'))
        return tabs


################################################################################
# ArticlePage
################################################################################


class ArticlePage(BasePage):

    """ArticlePage is a generic content page.

    """

    parent_page_types: list = ['core.SectionPage', ]
    subpage_types: list = []
