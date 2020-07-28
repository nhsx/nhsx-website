import pytest
import json

from django.test import Client
from .blocks import LINK_BLOCK
from taggit.models import Tag

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
        assert section_page.subnav_pages[index]["title"] == article_page.title
        assert section_page.subnav_pages[index]["url"] == article_page.url


def test_section_page_can_have_manually_specified_subnav_pages(
    section_page, article_pages
):
    section_page.automatic = False

    section_page.page_links = json.dumps([LINK_BLOCK, LINK_BLOCK])

    assert len(section_page.subnav_pages) == 2


def test_section_page_shows_subnav_pages(section_page):
    section_page.automatic = False

    section_page.page_links = json.dumps([LINK_BLOCK, LINK_BLOCK])

    section_page.save_revision().publish()

    rv = client.get(section_page.url)

    assert "http://example.com" in str(rv.content)


def test_section_page_with_two_page_links_has_half_width(section_page):
    section_page.automatic = False

    section_page.page_links = json.dumps([LINK_BLOCK, LINK_BLOCK])

    assert section_page.subnav_items_per_row() == 2
    assert section_page.subnav_column_class() == "one-half"


def test_section_page_with_three_page_links_has_third_width(section_page):
    section_page.automatic = False

    section_page.page_links = json.dumps([LINK_BLOCK, LINK_BLOCK, LINK_BLOCK])

    assert section_page.subnav_items_per_row() == 3
    assert section_page.subnav_column_class() == "one-third"


def test_section_page_with_four_page_links_has_half_width(section_page):
    section_page.automatic = False

    section_page.page_links = json.dumps(
        [LINK_BLOCK, LINK_BLOCK, LINK_BLOCK, LINK_BLOCK]
    )
    section_page.save_revision().publish()

    assert section_page.subnav_items_per_row() == 2
    assert section_page.subnav_column_class() == "one-half"


def test_section_page_hero_gets_output(section_page):
    p = section_page
    p.sub_head = "This is the hero sub head"
    p.save_revision().publish()
    rv = client.get(p.url)
    assert (
        '<p class="nhsuk-body-l nhsuk-u-margin-bottom-0">This is the hero sub head</p>'
        in rv.rendered_content
    )


def test_section_page_title_without_hero(section_page):
    p = section_page
    rv = client.get(p.url)
    assert (
        '<h1 class="nhsuk-heading-xl nhsuk-u-margin-bottom-5">Test Section Page</h1>'
        in rv.rendered_content
    )


def test_section_page_with_latest_blog_posts(section_page, blog_posts):
    """Test that we can list blog posts with a specific tag
        when using that block"""

    p = section_page

    tagged_posts = blog_posts[:3]

    for post in tagged_posts:
        post.tags.add("tag1")
        post.save_revision().publish()

    p.body = json.dumps(
        [
            {
                "type": "latest_blog_posts",
                "value": {
                    "heading": "Blog Posts",
                    "number_of_posts": "3",
                    "tag_id": Tag.objects.get(name="tag1").id,
                },
            }
        ]
    )
    p.save_revision().publish()

    rendered = p.body.render_as_block()

    assert "Blog Posts" in rendered

    for post in tagged_posts:
        assert post.title in rendered
