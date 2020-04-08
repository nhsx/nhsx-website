from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel

from modules.core.models.abstract import BasePage, BaseIndexPage, CanonicalMixin, PageTag
from modelcluster.contrib.taggit import ClusterTaggableManager


class NewsIndexPage(BaseIndexPage):
    subpage_types = ['News']
    max_count = 1


class News(BasePage, CanonicalMixin):
    parent_page_types = ['NewsIndexPage']

    tags = ClusterTaggableManager(through=PageTag, blank=True)

    settings_panels = CanonicalMixin.panels + BasePage.settings_panels

    content_panels = [
        *Page.content_panels,
        FieldPanel('first_published_at'),
        StreamFieldPanel("body"),
        FieldPanel("tags"),
    ]
