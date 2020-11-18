# 3rd party
from django.db import models

from wagtail.core import fields
from wagtail.admin.edit_handlers import StreamFieldPanel, FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.utils.decorators import cached_classmethod
from wagtail.core.models import Page

# Project
from modules.core.blocks import nhsx_blocks

# Module
from .abstract import BasePage, InlineHeroMixin, SidebarMixin, SubNavMixin

from modules.core.blocks import section_page_blocks

################################################################################
# SectionPage
################################################################################


class SectionPage(BasePage, InlineHeroMixin, SubNavMixin):

    """SectionPage is a top level page for containing grouped articles.

    """

    parent_page_types: list = [
        "home.HomePage",
        "core.SectionPage",
        "ai_lab.AiLabHomePage",
    ]
    subpage_types: list = [
        "core.ArticlePage",
        "core.SectionPage",
        "core.CookieFormPage",
        "people.PeopleListingPage",
        "meeting_minutes.MeetingMinutesListingPage",
        "ig_guidance.GuidanceListingPage",
        "case_studies.CaseStudyPage",
    ]

    subnav_panels: list = SubNavMixin.panels

    search_fields = BasePage.search_fields + InlineHeroMixin.extra_search_fields

    body = fields.StreamField(
        section_page_blocks, blank=True, verbose_name="Body blocks"
    )
    page_width = models.CharField(
        choices=[("two-thirds", "Two Thirds"), ("full", "Full")],
        max_length=20,
        default="two-thirds",
    )

    @cached_classmethod
    def get_admin_tabs(cls):
        tabs = super().get_admin_tabs()
        tabs.insert(2, (cls.subnav_panels, "Subnavigation"))
        return tabs

    def subnav_items_per_row(self):
        if len(self.subnav_pages) % 3 == 0:
            return 3
        else:
            return 2

    def subnav_column_class(self):
        if len(self.subnav_pages) % 3 == 0:
            return "one-third"
        else:
            return "one-half"

    content_panels = [
        *Page.content_panels,
        FieldPanel("sub_head"),
        ImageChooserPanel("image"),
        StreamFieldPanel("body"),
    ]

    settings_panels = [*Page.settings_panels, FieldPanel("page_width")]


################################################################################
# ArticlePage
################################################################################


class ArticlePage(BasePage, SidebarMixin):

    """ArticlePage is a generic content page.

    """

    parent_page_types: list = [
        "core.SectionPage",
        "home.HomePage",
        "ai_lab.AiLabHomePage",
    ]
    subpage_types: list = []

    sidebar_panels: list = SidebarMixin.panels

    @cached_classmethod
    def get_admin_tabs(cls):
        tabs = super().get_admin_tabs()
        tabs.insert(1, (cls.sidebar_panels, "Sidebar"))
        return tabs


################################################################################
# CookieFormPage
################################################################################


class CookieFormPage(ArticlePage):

    """CookieFormPage is a page type specifically for cookie consent content. It
    includes a form that sets Cookies in the template core/cookie_form_page.html
    """

    max_count = 1
