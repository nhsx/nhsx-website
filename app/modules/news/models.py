from modules.core.models.abstract import BasePage, BaseIndexPage, CanonicalMixin


class NewsIndexPage(BaseIndexPage):
    subpage_types = ['News']
    max_count = 1


class News(BasePage, CanonicalMixin):
    parent_page_types = ['NewsIndexPage']

    settings_panels = CanonicalMixin.panels + BasePage.settings_panels
