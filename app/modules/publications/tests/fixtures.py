from typing import List
import pytest

from wagtail.core.models import Page
from modules.publications.models import PublicationPage, PublicationIndexPage
from wagtail.tests.utils.form_data import rich_text, streamfield, nested_form_data
from wagtail.core.blocks.stream_block import StreamValue
import wagtail.core.blocks.stream_block
from wagtail.core.blocks import RichTextBlock

pytestmark = pytest.mark.django_db


def _create_publication_page(title: str, parent: Page) -> PublicationPage:
    """Abstracting this allows us to test more scenarios than just passing the
    fixture around.

    Args:
        title (str): The page title
        parent (Page): A page to attach our post to

    Returns:
        PublicationPage: Description
    """
    p = PublicationPage()
    p.title = title
    parent.add_child(instance=p)
    p.save_revision().publish()
    return p


def _create_publication_index_page(title: str, parent: Page) -> PublicationIndexPage:
    """Abstracting this allows us to test more scenarios than just passing the
    fixture around.

    Args:
        title (str): The page title
        parent (Page): A page to attach our post index page to

    Returns:
        PublicationIndexPage: Description
    """
    p = PublicationIndexPage()
    p.title = title
    parent.add_child(instance=p)
    p.save_revision().publish()
    return p


@pytest.fixture(scope="function")
def publication_index_page(home_page) -> PublicationIndexPage:
    p = _create_publication_index_page("Test Publication Index Page", home_page)
    return p


@pytest.fixture(scope="function")
def publication_page(publication_index_page) -> PublicationPage:
    p = _create_publication_page("Test Publication Page", publication_index_page)
    return p


@pytest.fixture(scope="function")
def publication_pages(publication_index_page) -> List[PublicationPage]:
    """Fixture providing 10 PublicationPage objects attached to publication_index_page"""
    rv = []
    for _ in range(0, 10):
        p = _create_publication_page(
            f"Test Publication Page {_}", publication_index_page
        )
        rv.append(p)
    return rv
