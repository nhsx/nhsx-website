from modules.core.models.abstract import BasePage, BaseIndexPage

class BlogPostIndexPage(BaseIndexPage):
    subpage_types = [ 'BlogPost' ]

class BlogPost(BasePage):
    parent_page_types = ['BlogPostIndexPage']

