import json
import re
import pytest
from django.test import Client, TestCase
from django.core.management.commands import loaddata
from modules.longform.models import LongformPost


pytestmark = pytest.mark.django_db
client = Client()


def test_longform_streamfield_has_anchors(longform_post):
    longform_post.body = json.dumps(
        [
            {
                "type": "rich_text",
                "value": "<h2>A title</h2><p>Some Text</p><h2>A title</h2>",
            },
            {
                "type": "rich_text",
                "value": "<h2>A title</h2>      <h2>A different title</h2>",
            },
        ]
    )
    longform_post.save_revision().publish()
    rv = client.get(longform_post.url)
    assert '<h2 id="a-title">' in rv.rendered_content
    assert '<h2 id="a-title-2">' in rv.rendered_content
    assert '<h2 id="a-title-3">' in rv.rendered_content
    assert '<h2 id="a-different-title">' in rv.rendered_content
    assert "<a href='#a-title'>" in rv.rendered_content
    assert "<a href='#a-title-2'>" in rv.rendered_content
    assert "<a href='#a-title-3'>" in rv.rendered_content
    assert "<a href='#a-different-title'>" in rv.rendered_content


def test_longform_post_gets_created(longform_post):
    """Test that we have a longform post created by the fixture
    """
    assert longform_post is not None


def test_longform_post_200(longform_post):
    """Test that we have a longform post created by the fixture
    """
    rv = client.get(longform_post.url)
    assert rv.status_code == 200


@pytest.mark.skip(reason="tags not implemented yet")
def test_longform_post_shows_tags(longform_post):
    """Test that we can see a longform post's tags
    """
    longform_post.tags.add("This is a tag")
    longform_post.save_revision().publish()

    rv = client.get(longform_post.url)

    assert "This is a tag" in str(rv.content)


def test_longform_post_users_list(longform_post, users):
    """Test that longform posts can list a user's full names
    """
    longform_post.authors.add(users[0])
    longform_post.authors.add(users[1])

    longform_post.save()

    rv = client.get(longform_post.url)

    assert "User 0" in rv.rendered_content
    assert "User 1" in rv.rendered_content


def test_longform_post_users_list_with_salutations_and_job_titles(
    longform_post, authors
):
    """Test that longform posts can list a user's full names with job title and salutation
    """
    longform_post.authors.add(authors[0])
    longform_post.authors.add(authors[1])

    longform_post.save()

    rv = client.get(longform_post.url)

    assert "Dr. Firsty Lasty (Doctor)" in rv.rendered_content
    assert "Prof. Fname Lname (Professor)" in rv.rendered_content
