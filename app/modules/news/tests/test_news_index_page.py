import pytest

from django.test import Client

pytestmark = pytest.mark.django_db

client = Client()


def test_news_index_page_gets_created(news_index_page):
    """Test that we have a news index page created by the fixture"""
    assert news_index_page is not None


def test_news_index_page_can_have_hero_content(news_index_page):
    """Test that news index pages can have hero content"""
    news_index_page.headline = "This is a headline"
    news_index_page.sub_head = "Some subheading"

    # TODO: How do we test this?
    # news_index_page.image = ???
    news_index_page.save_revision().publish()

    news_index_page.refresh_from_db()

    assert news_index_page.headline == "This is a headline"
    assert news_index_page.sub_head == "Some subheading"


def test_news_index_page_has_a_subhead_and_image_option(news_index_page):
    """Check that hero content can be editable in the admin section"""
    assert news_index_page.get_admin_tabs()[0][0][1].field_name == "sub_head"
    assert news_index_page.get_admin_tabs()[0][0][2].field_name == "image"


def test_news_index_page_get_children(news_index_page, news_items):
    """Check that news_index_page has 10 children"""
    assert len(news_index_page.get_children()) == 10


def test_news_index_200(news_index_page):
    """Test that we have a news index page created by the fixture"""
    rv = client.get(news_index_page.url)
    assert rv.status_code == 200


def test_news_index_lists_news(news_index_page, news_items):
    """Test that the index page lists all of the news items"""
    rv = client.get(news_index_page.url)

    for news_item in news_items:
        assert news_item.title in str(rv.content)


def test_news_index_shows_tags(news_index_page, news_items):
    """Test that we can see a blog post's tags"""
    news_items[0].tags.add("This is a tag")
    news_items[0].save_revision().publish()

    rv = client.get(news_index_page.url)

    assert "This is a tag" in str(rv.content)
