# 3rd party
import json
from typing import List
import pytest
from wagtail.core.models import Page
from modules.core.models import SectionPage, ArticlePage

from .blocks import RICHTEXT_BLOCK

pytestmark = pytest.mark.django_db


def _create_section_page(title: str, parent: Page) -> SectionPage:
    """Abstracting this allows us to test more scenarios than just passing the
    fixture around.

    Args:
        title (str): The page title
        parent (Page): A page to attach our section page to

    Returns:
        SectionPage: Description
    """
    p = SectionPage()
    p.title = title
    parent.add_child(instance=p)
    p.save_revision().publish()
    return p


def _create_article_page(title: str, parent: Page) -> SectionPage:
    """Abstracting this allows us to test more scenarios than just passing the
    fixture around.

    Args:
        title (str): The page title
        parent (Page): A page to attach our article page to

    Returns:
        SectionPage: Description
    """
    p = ArticlePage()
    p.title = title
    parent.add_child(instance=p)
    p.save_revision().publish()
    return p


@pytest.fixture(scope="function")
def section_page(home_page) -> SectionPage:
    p = _create_section_page('Test Section Page', home_page)
    return p


@pytest.fixture(scope="function")
def article_page(section_page) -> ArticlePage:
    p = _create_article_page('Test Article Page', section_page)
    return p


@pytest.fixture(scope="function")
def article_pages(section_page) -> List[ArticlePage]:
    """Fixture providing 10 ArticlePages attached to section_page
    """
    rv = []
    for _ in range(0, 10):
        p = _create_article_page(f'Test Article Page {_}', section_page)
        rv.append(p)
    return rv


@pytest.fixture(scope="function")
def article_page_with_body(section_page) -> ArticlePage:
    p = _create_article_page('Test Article Page', section_page)
    p.body = json.dumps([
        RICHTEXT_BLOCK
    ])
    p.save_revision().publish()
    return p
