# -*- coding: utf-8 -*-

"""
    core.models.abstract
    ~~~~~~~~~~~~~~~~~~~~
    Concrete models and mixins for extending page functionality. This code structure helps
    us keep things DRY by creating classes that provide functionality to mutliple page types.

    If you need to add functionality that _every_ page type should get, add it to `BasePage`.
    If you need to add functionality that _some_ page types should get, add a mixin.
    If you need to add functionality that _one_ page type should get, add it to the page model.

"""

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
