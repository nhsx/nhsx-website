# stdlib
import logging
import re
import lxml.html
import hashlib
import random

# 3rd party
from django.db import models
from wagtail.core import fields
from taggit.models import TaggedItemBase
from wagtail.search import index
from dal_select2.widgets import ModelSelect2Multiple
from modelcluster.fields import ParentalKey
from wagtail.core.models import Page
from wagtail.utils.decorators import cached_classmethod
from modelcluster.contrib.taggit import ClusterTaggableManager
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from django.views.decorators.cache import cache_page

# Project
from modules.core.models.abstract import (
    BasePage,
    BaseIndexPage,
    CanonicalMixin,
    PageAuthorsMixin,
)


logger = logging.getLogger(__name__)


def make_stub(name):
    # TODO make unique even if name same
    # TODO make stub meaningful to humans
    return hashlib.sha1(name.encode("utf-8")).hexdigest()[:8]


def replace_headers(html):
    """Make headers provide id attributes so they can be used as anchors
    and provide a list of them to build a table of contents."""
    header_tags = ["h2"]
    toc = []
    root = lxml.html.fromstring(html)
    for tag_name in header_tags:
        for tag in root.xpath(f"//{tag_name}"):
            header_name = tag.text
            stub = make_stub(header_name)
            tag.set("id", stub)
            toc.append((header_name, stub))
    return lxml.html.tostring(root).decode("utf-8"), toc


################################################################################
# Page models
################################################################################


class LongformPost(BasePage, PageAuthorsMixin, CanonicalMixin):
    # standard approach appears to be
    # (via https://docs.wagtail.io/en/latest/topics/streamfield.html)
    # author = models.Charfield(max_length=255)
    # which also gives subcategories for StreamField
    parent_page_types = ["LongformPostIndexPage"]
    subpage_types = []

    content_panels = [
        *Page.content_panels,
        FieldPanel("first_published_at"),
        FieldPanel("authors", widget=ModelSelect2Multiple(url="author-autocomplete")),
        StreamFieldPanel("body"),
    ]

    settings_panels = CanonicalMixin.panels + BasePage.settings_panels

    def get_context(self, request):
        print(self.body.stream_block._constructor_args[0][0][0][1].__dict__)
        context = super().get_context(request)
        context["toc"] = []
        context["repr"] = ""
        html_list = []
        for block in self.body._raw_data:
            # TODO consider diving deeper into expander nodes
            if block["type"] == "rich_text":
                replacement_html, new_toc = replace_headers(block["value"])
                context["toc"].extend(new_toc)
                html_list.append(replacement_html)
            else:
                html_list.append(block["value"])
        for i, html in enumerate(html_list):
            self.body._raw_data[i]["value"] = html
            # TODO consider changing id?

        return context


class LongformPostIndexPage(BaseIndexPage):
    _child_model = LongformPost

    subpage_types = ["LongformPost"]
    max_count = 1
