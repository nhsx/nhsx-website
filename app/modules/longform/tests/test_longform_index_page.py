import pytest
from django.test import Client

pytestmark = pytest.mark.django_db

client = Client()


def test_longform_post_index_page_gets_created(longform_post_index_page):
    """Test that we have a longform post index page created by the fixture
    """
    assert longform_post_index_page is not None


def test_longform_post_index_page_can_have_hero_content(longform_post_index_page):
    """Test that longform post index pages can have hero content
    """
    longform_post_index_page.headline = "This is a headline"
    longform_post_index_page.sub_head = "Some subheading"

    # TODO: How do we test this?
    # longform_post_index_page.image = ???
    longform_post_index_page.save_revision().publish()

    longform_post_index_page.refresh_from_db()

    assert longform_post_index_page.headline == "This is a headline"
    assert longform_post_index_page.sub_head == "Some subheading"


def test_longform_post_index_page_has_a_subhead_and_image_option(
    longform_post_index_page,
):
    """Check that hero content can be editable in the admin section
    """
    assert longform_post_index_page.get_admin_tabs()[0][0][1].field_name == "sub_head"
    assert longform_post_index_page.get_admin_tabs()[0][0][2].field_name == "image"


def test_longform_post_index_page_get_children(
    longform_post_index_page, longform_posts
):
    """Check that longform_post_index_page has 10 children
    """
    assert len(longform_post_index_page.get_children()) == 10


def test_longform_post_index_200(longform_post_index_page):
    """Test that we have a longform post index page created by the fixture
    """
    rv = client.get(longform_post_index_page.url)
    assert rv.status_code == 200


def test_longform_post_index_lists_longform_posts(
    longform_post_index_page, longform_posts
):
    """Test that the index page lists all of the longform posts
    """
    rv = client.get(longform_post_index_page.url)

    for longform_post in longform_posts:
        assert longform_post.title in str(rv.content)


@pytest.mark.skip(reason="tags not implemented yet")
def test_longform_post_index_shows_tags(longform_post):
    """Test that we can see a longform post's tags
    """
    longform_post.tags.add("This is a tag")
    longform_post.save_revision().publish()

    rv = client.get(longform_post.get_parent().url)

    assert "This is a tag" in str(rv.content)


@pytest.mark.skip(reason="tags not implemented yet")
def test_longform_post_index_filters_by_tag(longform_post_index_page, longform_posts):
    longform_posts[0].tags.add("tag1")
    longform_posts[0].save_revision().publish()

    longform_posts[1].tags.add("tag2")
    longform_posts[1].save_revision().publish()

    rv = client.get(longform_post_index_page.url + "?tag=tag1")

    assert longform_posts[0].title in str(rv.content)
    assert longform_posts[1].title not in str(rv.content)


@pytest.mark.skip(reason="tags not implemented yet")
def test_longform_post_index_filters_by_multiple_tags(
    longform_post_index_page, longform_posts
):

    longform_posts[0].tags.add("tag1")
    longform_posts[0].save_revision().publish()

    longform_posts[1].tags.add("tag2")
    longform_posts[1].save_revision().publish()

    longform_posts[2].tags.add("tag3")
    longform_posts[2].save_revision().publish()

    rv = client.get(longform_post_index_page.url + "?tag=tag1,tag2")

    assert longform_posts[0].title in str(rv.content)
    assert longform_posts[1].title in str(rv.content)
    assert longform_posts[2].title not in str(rv.content)


def test_longform_post_index_page_shows_user_names(
    longform_post_index_page, longform_posts, user
):
    """Test that we can see a longform post's tags
    """
    longform_posts[0].authors.add(user)
    longform_posts[0].save_revision().publish()

    rv = client.get(longform_post_index_page.url)

    assert user.full_name in str(rv.content)
