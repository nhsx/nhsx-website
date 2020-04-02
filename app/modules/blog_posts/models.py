from modules.core.models.abstract import BasePage, BaseIndexPage

class BlogPostIndexPage(BaseIndexPage):
    pass

class BlogPost(BasePage):
    parent_page_types = ['BlogPostIndexPage']

