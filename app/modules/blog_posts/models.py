from modules.core.models.abstract import BasePage, BaseIndexPage

class BlogPostIndexPage(BaseIndexPage):
    subpage_types = [ 'BlogPost' ]
    max_count = 1

class BlogPost(BasePage):
    parent_page_types = ['BlogPostIndexPage']

