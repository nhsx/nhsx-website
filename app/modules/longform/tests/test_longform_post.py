import pytest
from django.test import Client, TestCase
from django.core.management.commands import loaddata

pytestmark = pytest.mark.django_db

client = Client()


@pytest.mark.skip(reason="placeholder")
class FixtureTestCase(TestCase):
    # docs.django.com/en/3.0/topics/testing/tools#topics-testing-fixtures
    fixtures = ["dbdump.json"]

    def test_longform_is_complicated(longform_post):
        raise RuntimeError("expected failure")


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
