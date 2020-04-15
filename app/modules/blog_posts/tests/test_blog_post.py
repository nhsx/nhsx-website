import pytest
from django.test import Client

pytestmark = pytest.mark.django_db

client = Client()


def test_blog_post_gets_created(blog_post):
    """Test that we have a blog post created by the fixture
    """
    assert blog_post is not None


def test_blog_post_200(blog_post):
    """Test that we have a blog post created by the fixture
    """
    rv = client.get(blog_post.url)
    assert rv.status_code == 200


def test_blog_post_shows_tags(blog_post):
    """Test that we can see a blog post's tags
    """
    blog_post.tags.add("This is a tag")
    blog_post.save_revision().publish()

    rv = client.get(blog_post.url)

    assert "This is a tag" in str(rv.content)


def test_blog_post_users_list(blog_post, users):
    """Test that blog posts can list a user's full names
    """
    blog_post.authors.add(users[0])
    blog_post.authors.add(users[1])

    blog_post.save()

    rv = client.get(blog_post.url)

    assert "User 0" in rv.rendered_content
    assert "User 1" in rv.rendered_content
