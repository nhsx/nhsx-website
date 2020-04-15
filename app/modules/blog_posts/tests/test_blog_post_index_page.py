import pytest
from django.test import Client

pytestmark = pytest.mark.django_db

client = Client()


def test_blog_post_index_page_gets_created(blog_post_index_page):
    """Test that we have a blog post index page created by the fixture
    """
    assert blog_post_index_page is not None


def test_blog_post_index_page_can_have_hero_content(blog_post_index_page):
    """Test that blog post index pages can have hero content
    """
    blog_post_index_page.headline = "This is a headline"
    blog_post_index_page.sub_head = "Some subheading"

    # TODO: How do we test this?
    # blog_post_index_page.image = ???
    blog_post_index_page.save_revision().publish()

    blog_post_index_page.refresh_from_db()

    assert blog_post_index_page.headline == "This is a headline"
    assert blog_post_index_page.sub_head == "Some subheading"


def test_blog_post_index_page_has_a_subhead_and_image_option(blog_post_index_page):
    """Check that hero content can be editable in the admin section
    """
    assert blog_post_index_page.get_admin_tabs()[0][0][1].field_name == "sub_head"
    assert blog_post_index_page.get_admin_tabs()[0][0][2].field_name == "image"


def test_blog_post_index_page_get_children(blog_post_index_page, blog_posts):
    """Check that blog_post_index_page has 10 children
    """
    assert len(blog_post_index_page.get_children()) == 10


def test_blog_post_index_200(blog_post_index_page):
    """Test that we have a blog post index page created by the fixture
    """
    rv = client.get(blog_post_index_page.url)
    assert rv.status_code == 200


def test_blog_post_index_lists_blog_posts(blog_post_index_page, blog_posts):
    """Test that the index page lists all of the blog posts
    """
    rv = client.get(blog_post_index_page.url)

    for blog_post in blog_posts:
        assert blog_post.title in str(rv.content)


def test_blog_post_index_shows_tags(blog_post):
    """Test that we can see a blog post's tags
    """
    blog_post.tags.add("This is a tag")
    blog_post.save_revision().publish()

    rv = client.get(blog_post.get_parent().url)

    assert "This is a tag" in str(rv.content)


def test_blog_post_index_filters_by_tag(blog_post_index_page, blog_posts):

    blog_posts[0].tags.add("tag1")
    blog_posts[0].save_revision().publish()

    blog_posts[1].tags.add("tag2")
    blog_posts[1].save_revision().publish()

    rv = client.get(blog_post_index_page.url + "?tag=tag1")

    assert blog_posts[0].title in str(rv.content)
    assert blog_posts[1].title not in str(rv.content)


def test_blog_post_index_filters_by_multiple_tags(blog_post_index_page, blog_posts):

    blog_posts[0].tags.add("tag1")
    blog_posts[0].save_revision().publish()

    blog_posts[1].tags.add("tag2")
    blog_posts[1].save_revision().publish()

    blog_posts[2].tags.add("tag3")
    blog_posts[2].save_revision().publish()

    rv = client.get(blog_post_index_page.url + "?tag=tag1,tag2")

    assert blog_posts[0].title in str(rv.content)
    assert blog_posts[1].title in str(rv.content)
    assert blog_posts[2].title not in str(rv.content)


def test_blog_post_index_page_shows_user_names(blog_post_index_page, blog_posts, user):
    """Test that we can see a blog post's tags
    """
    blog_posts[0].authors.add(user)
    blog_posts[0].save_revision().publish()

    rv = client.get(blog_post_index_page.url)

    assert user.full_name in str(rv.content)
