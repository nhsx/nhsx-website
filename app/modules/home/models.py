
# Project
from modules.core.models import BasePage


class HomePage(BasePage):

    @classmethod
    def can_create_at(cls, parent):
        """This stops admin users from creating more than one HomePage.
        """
        return super().can_create_at(parent) \
            and not cls.objects.exists()
