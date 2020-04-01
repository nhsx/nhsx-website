# 3rd party
from wagtail.core import fields

# Project
from modules.core.blocks import nhsx_blocks
from modules.core.models import BasePage
from wagtail.admin.edit_handlers import StreamFieldPanel


class HomePage(BasePage):

    @classmethod
    def can_create_at(cls, parent):
        """This stops admin users from creating more than one HomePage.
        """
        return super().can_create_at(parent) \
            and not cls.objects.exists()
