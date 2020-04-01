import pytest
from django.test import Client


pytestmark = pytest.mark.django_db

client = Client()


def test_article_page_gets_created(article_page):
    """Test that we have a article page created by the fixture
    """
    assert article_page is not None


def test_article_page_200(article_page):
    """Test that the article page is reachable and returns a 200
    """
    rv = client.get(article_page.url)
    assert rv.status_code == 200
