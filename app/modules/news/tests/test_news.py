import pytest
from django.test import Client

pytestmark = pytest.mark.django_db

client = Client()

def test_news_page_gets_created(news_page):
    """Test that we have a news page created by the fixture
    """
    assert news_page is not None

def test_news_200(news_page):
    """Test that we have a news page created by the fixture
    """
    rv = client.get(news_page.url)
    assert rv.status_code == 200
