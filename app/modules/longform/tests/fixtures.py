from typing import List
import pytest

from wagtail.core.models import Page
from modules.longform.models import LongformPost, LongformPostIndexPage
from wagtail.tests.utils.form_data import rich_text, streamfield, nested_form_data
from wagtail.core.blocks.stream_block import StreamValue
import wagtail.core.blocks.stream_block
from wagtail.core.blocks import RichTextBlock

pytestmark = pytest.mark.django_db


def replacement(self, item):
    if isinstance(item, StreamValue.StreamChild):
        return item

    try:
        type_name, value, block_id = item
    except ValueError:
        type_name, value = item
        block_id = None

    print(self.stream_block.child_blocks.keys())
    block_def = self.stream_block.child_blocks[type_name]


wagtail.core.blocks.stream_block._construct_stream_child = replacement


def _create_longform_post(title: str, parent: Page) -> LongformPost:
    """Abstracting this allows us to test more scenarios than just passing the
    fixture around.

    Args:
        title (str): The page title
        parent (Page): A page to attach our post to

    Returns:
        LongformPost: Description
    """
    p = LongformPost()
    p.title = title
    parent.add_child(instance=p)
    p.save_revision().publish()
    return p


def _create_longform_post_index_page(title: str, parent: Page) -> LongformPostIndexPage:
    """Abstracting this allows us to test more scenarios than just passing the
    fixture around.

    Args:
        title (str): The page title
        parent (Page): A page to attach our post index page to

    Returns:
        LongformPostIndexPage: Description
    """
    p = LongformPostIndexPage()
    print(p.get_children())
    p.title = title
    parent.add_child(instance=p)
    p.save_revision().publish()
    return p


@pytest.fixture(scope="function")
def longform_post_index_page(home_page) -> LongformPostIndexPage:
    p = _create_longform_post_index_page("Test Longform Post Index Page", home_page)
    return p


@pytest.fixture(scope="function")
def longform_post(longform_post_index_page) -> LongformPost:
    p = _create_longform_post("Test Longform Post", longform_post_index_page)
    return p


@pytest.fixture(scope="function")
def longform_posts(longform_post_index_page) -> List[LongformPost]:
    """Fixture providing 10 LongformPost objects attached to longform_post_index_page
    """
    rv = []
    for _ in range(0, 10):
        p = _create_longform_post(f"Test Longform Post {_}", longform_post_index_page)
        rv.append(p)
    return rv
