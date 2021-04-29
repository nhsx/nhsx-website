import pytest
from django.test import Client

pytestmark = pytest.mark.django_db

client = Client()


def test_publication_index_page_gets_created(publication_index_page):
    """Test that we have a publication index page created by the fixture
    """
    assert publication_index_page is not None


def test_publication_index_page_can_have_hero_content(publication_index_page):
    """Test that publication index pages can have hero content
    """
    publication_index_page.headline = "This is a headline"
    publication_index_page.sub_head = "Some subheading"

    # TODO: How do we test this?
    # publication_index_page.image = ???
    publication_index_page.save_revision().publish()

    publication_index_page.refresh_from_db()

    assert publication_index_page.headline == "This is a headline"
    assert publication_index_page.sub_head == "Some subheading"


def test_publication_index_page_has_a_subhead_and_image_option(publication_index_page,):
    """Check that hero content can be editable in the admin section
    """
    assert publication_index_page.get_admin_tabs()[0][0][1].field_name == "sub_head"
    assert publication_index_page.get_admin_tabs()[0][0][2].field_name == "image"


def test_publication_index_page_get_children(publication_index_page, publication_pages):
    """Check that publication_index_page has 10 children
    """
    assert len(publication_index_page.get_children()) == 10


def test_publication_index_page_200(publication_index_page):
    """Test that we have a publication index page created by the fixture
    """
    rv = client.get(publication_index_page.url)
    assert rv.status_code == 200


def test_publication_index_page_lists_publication_pages(
    publication_index_page, publication_pages
):
    """Test that the index page lists all of the publication pages
    """
    rv = client.get(publication_index_page.url)

    for publication_page in publication_pages:
        assert publication_page.title in str(rv.content)
