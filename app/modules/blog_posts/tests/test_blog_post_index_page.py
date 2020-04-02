import pytest
from django.test import Client

pytestmark = pytest.mark.django_db

client = Client()

def test_blog_post_index_page_gets_created(blog_post_index_page):
    """Test that we have a blog post index page created by the fixture
    """
    assert blog_post_index_page is not None

def test_blog_post_index_page_get_children(blog_post_index_page, blog_posts):
    """Check that blog_post_index_page has 10 children
    """
    assert len(blog_post_index_page.get_children()) == 10
