# 3rd party
from wagtail.core import fields

# Project
from modules.core.blocks import nhsx_blocks

# Module
from .abstract import BasePage


################################################################################
# SectionPage
################################################################################


class SectionPage(BasePage):
    body = fields.StreamField(
        nhsx_blocks, blank=True, verbose_name="Body blocks"
    )


################################################################################
# ArticlePage
################################################################################


class ArticlePage(BasePage):
    body = fields.StreamField(
        nhsx_blocks, blank=True, verbose_name="Body blocks"
    )
