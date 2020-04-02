import pytest
from django.test import Client

pytestmark = pytest.mark.django_db

client = Client()

def test_news_index_page_gets_created(news_index_page):
    """Test that we have a news index page created by the fixture
    """
    assert news_index_page is not None

def test_news_index_page_get_children(news_index_page, news_items):
    """Check that news_index_page has 10 children
    """
    assert len(news_index_page.get_children()) == 10
