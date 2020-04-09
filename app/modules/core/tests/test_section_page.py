import pytest
import json

from django.test import Client
from .blocks import LINK_BLOCK

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

def section_page_can_have_section_pages_as_children(section_page, section_pages):
    """Check that section_page can have other section pages as children
    """
    assert len(section_page.get_children()) == 10

def test_section_page_can_have_automatic_subnav_pages(section_page, article_pages):
    section_page.automatic = True

    assert len(section_page.subnav_pages) == 10

    for index, article_page in enumerate(article_pages):
        assert section_page.subnav_pages[index]['title'] == article_page.title
        assert section_page.subnav_pages[index]['url'] == article_page.url

def test_section_page_can_have_manually_specified_subnav_pages(section_page, article_pages):
    section_page.automatic = False

    section_page.page_links = json.dumps([
        LINK_BLOCK,
        LINK_BLOCK
    ])

    assert len(section_page.subnav_pages) == 2

def test_section_page_shows_subnav_pages(section_page):
    section_page.automatic = False

    section_page.page_links = json.dumps([
        LINK_BLOCK,
        LINK_BLOCK
    ])

    section_page.save_revision().publish()

    rv = client.get(section_page.url)

    assert "http://example.com" in str(rv.content)






