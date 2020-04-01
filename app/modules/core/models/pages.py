# 3rd party
from wagtail.core import fields
from wagtail.admin.edit_handlers import StreamFieldPanel

# Project
from modules.core.blocks import nhsx_blocks

# Module
from .abstract import BasePage


################################################################################
# SectionPage
################################################################################


class SectionPage(BasePage):

    """SectionPage is a top level page for containing grouped articles.

    """

    parent_page_types = ['home.HomePage', ]
    child_page_types = ['core.ArticlePage', ]


################################################################################
# ArticlePage
################################################################################


class ArticlePage(BasePage):

    """ArticlePage is a generic content page.

    """
    pass
