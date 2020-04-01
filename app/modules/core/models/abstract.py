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

from typing import List
from consoler import console

# 3rd party
from django.utils.text import slugify
from wagtail.core.models import Page
from django.utils.translation import ugettext_lazy as _  # NOQA
from wagtail.utils.decorators import cached_classmethod
from wagtail.admin.edit_handlers import ObjectList, TabbedInterface, StreamFieldPanel


################################################################################
# Base Page
################################################################################


class BasePage(Page):

    """Make sure any new pages you create extend this one, so that there is a
    centralised place where we can add functionality to all page types.
    """

    class Meta:
        abstract = True

    content_panels = Page.content_panels
    promote_panels = Page.promote_panels
    settings_panels = Page.settings_panels

    @cached_classmethod
    def get_admin_tabs(cls) -> List[tuple]:
        """Extend the admin tabs in your subclass page by calling this and then
        editing the returned list. Alternatively, leave all of this out of your subclass
        to get the BasePage tabs.

        Example:
            @cached_classmethod
            def get_admin_tabs(cls):
                tabs = super().get_admin_tabs()
                tabs.insert(3, (cls.taxonomy_panels, 'Taxonomy'))
                return tabs

        Returns:
            list: List of tuples
        """
        console.warn('WUT', cls)
        tabs = [
            (cls.content_panels, 'Content'),
            (cls.promote_panels, 'Promote'),
            (cls.settings_panels, 'Settings'),
        ]
        return tabs

    @cached_classmethod
    def get_edit_handler(cls) -> TabbedInterface:  # NOQA
        """s
        """
        tabs = cls.get_admin_tabs()
        edit_handler = TabbedInterface([
            ObjectList(tab[0], heading=tab[1], classname=slugify(tab[1])) for tab in tabs
        ])
        return edit_handler.bind_to(model=cls)
