# 3rd party
from wagtail.core.models import Page
from django.utils.translation import ugettext_lazy as _  # NOQA


################################################################################
# Base Page
################################################################################


class BasePage(Page):

    """Make sure any new pages you create extend this one, so that there is a
    centralised place where we can add functionality to all page types.
    """

    class Meta:
        abstract = True
