from modules.core.models.abstract import BasePage, BaseIndexPage

class NewsIndexPage(BaseIndexPage):
    pass

class News(BasePage):
    parent_page_types = ['NewsIndexPage']

