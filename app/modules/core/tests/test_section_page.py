import pytest
from django.test import Client


pytestmark = pytest.mark.django_db

client = Client()


def test_section_page_gets_created(section_page):
    """Test that we have a section page created by the fixture
    """
    assert section_page is not None


def test_section_page_200(section_page):
    """Test that the section page is reachable and returns a 200
    """
    rv = client.get(section_page.url)
    assert rv.status_code == 200


def test_section_page_get_children(section_page, article_pages):
    """Check that section_page has 10 children
    """
    assert len(section_page.get_children()) == 10
