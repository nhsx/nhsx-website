from typing import List
import pytest

from wagtail.core.models import Page
from modules.blog_posts.models import BlogPost, BlogPostIndexPage

pytestmark = pytest.mark.django_db

def _create_blog_post(title: str, parent: Page) -> BlogPost:
    """Abstracting this allows us to test more scenarios than just passing the
    fixture around.

    Args:
        title (str): The page title
        parent (Page): A page to attach our blog post to

    Returns:
        BlogPost: Description
    """
    p = BlogPost()
    p.title = title
    parent.add_child(instance=p)
    p.save_revision().publish()
    return p

def _create_blog_post_index_page(title: str, parent: Page) -> BlogPostIndexPage:
    """Abstracting this allows us to test more scenarios than just passing the
    fixture around.

    Args:
        title (str): The page title
        parent (Page): A page to attach our blog post index page to

    Returns:
        BlogPostIndexPage: Description
    """
    p = BlogPostIndexPage()
    p.title = title
    parent.add_child(instance=p)
    p.save_revision().publish()
    return p

@pytest.fixture(scope="function")
def blog_post_index_page(home_page) -> BlogPostIndexPage:
    p = _create_blog_post_index_page('Test Blog Post Index Page', home_page)
    return p

@pytest.fixture(scope="function")
def blog_post(blog_post_index_page) -> BlogPost:
    p = _create_blog_post('Test Blog Post', blog_post_index_page)
    return p

@pytest.fixture(scope="function")
def blog_posts(blog_post_index_page) -> List[BlogPost]:
    """Fixture providing 10 BlogPost objects attached to blog_post_index_page
    """
    rv = []
    for _ in range(0, 10):
        p = _create_blog_post(f'Test Blog Post {_}', blog_post_index_page)
        rv.append(p)
    return rv



