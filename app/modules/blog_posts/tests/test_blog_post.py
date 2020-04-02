import pytest
from django.test import Client

pytestmark = pytest.mark.django_db

client = Client()

def test_blog_post_gets_created(blog_post):
    """Test that we have a blog post created by the fixture
    """
    assert blog_post is not None

def test_blog_post_200(blog_post):
    """Test that we have a blog post created by the fixture
    """
    rv = client.get(blog_post.url)
    assert rv.status_code == 200
