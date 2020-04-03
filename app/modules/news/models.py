from modules.core.models.abstract import BasePage, BaseIndexPage

class NewsIndexPage(BaseIndexPage):
    subpage_types = ['News']

class News(BasePage):
    parent_page_types = ['NewsIndexPage']

