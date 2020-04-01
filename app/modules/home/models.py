# 3rd party
from wagtail.core import fields

# Project
from modules.core.blocks import nhsx_blocks
from modules.core.models import BasePage
from wagtail.admin.edit_handlers import StreamFieldPanel


class HomePage(BasePage):

    body = fields.StreamField(
        nhsx_blocks, blank=True, verbose_name="Body blocks"
    )

    content_panels = BasePage.content_panels + [
        StreamFieldPanel('body'),
    ]
