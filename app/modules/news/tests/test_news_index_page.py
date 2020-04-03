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

def test_news_index_200(news_index_page):
    """Test that we have a news index page created by the fixture
    """
    rv = client.get(news_index_page.url)
    assert rv.status_code == 200

def test_news_index_lists_news(news_index_page, news_items):
    """Test that the index page lists all of the news items
    """
    rv = client.get(news_index_page.url)

    for news_item in news_items:
        assert rv.content.find(str.encode(news_item.title))

