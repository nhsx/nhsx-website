import pytest
from django.test import Client

from modules.core.models import ArticlePage


pytestmark = pytest.mark.django_db

client = Client()


def test_article_page_gets_created(article_page):
    """Test that we have a article page created by the fixture
    """
    assert isinstance(article_page, ArticlePage)
    assert article_page is not None


def test_article_page_200(article_page):
    """Test that the article page is reachable and returns a 200
    """
    rv = client.get(article_page.url)
    assert rv.status_code == 200


def test_article_page_with_body(article_page_with_body):
    """Test that we have a article page created by the fixture
    """
    p = article_page_with_body
    assert isinstance(p, ArticlePage)
    assert p is not None
    rv = client.get(p.url)
    rendered = p.body.render_as_block()
    '<div class="block-rich_text">' in rendered
    assert 'Nullam quis risus eget' in rendered
    assert rv.status_code == 200
