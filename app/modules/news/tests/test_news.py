import pytest
from django.test import Client

pytestmark = pytest.mark.django_db

client = Client()

def test_news_page_gets_created(news_page):
    """Test that we have a news page created by the fixture
    """
    assert news_page is not None
