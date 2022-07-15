from typing import List
import pytest

from wagtail.models import Page
from modules.news.models import News, NewsIndexPage

pytestmark = pytest.mark.django_db


def _create_news_page(title: str, parent: Page) -> News:
    """Abstracting this allows us to test more scenarios than just passing the
    fixture around.

    Args:
        title (str): The page title
        parent (Page): A page to attach our article page to

    Returns:
        News: Description
    """
    p = News()
    p.title = title
    parent.add_child(instance=p)
    p.save_revision().publish()
    return p


def _create_news_index_page(title: str, parent: Page) -> NewsIndexPage:
    """Abstracting this allows us to test more scenarios than just passing the
    fixture around.

    Args:
        title (str): The page title
        parent (Page): A page to attach our article page to

    Returns:
        NewsIndexPage: Description
    """
    p = NewsIndexPage()
    p.title = title
    parent.add_child(instance=p)
    p.save_revision().publish()
    return p


@pytest.fixture(scope="function")
def news_index_page(home_page) -> NewsIndexPage:
    p = _create_news_index_page("Test Section Page", home_page)
    return p


@pytest.fixture(scope="function")
def news_page(news_index_page) -> News:
    p = _create_news_page("Test News Item", news_index_page)
    return p


@pytest.fixture(scope="function")
def news_items(news_index_page) -> List[News]:
    """Fixture providing 10 News objects attached to news_index_page"""
    rv = []
    for _ in range(0, 10):
        p = _create_news_page(f"Test News Page {_}", news_index_page)
        rv.append(p)
    return rv
