import json
import re
import pytest
from django.test import Client, TestCase
from django.core.management.commands import loaddata
from modules.longform.models import LongformPost
from datetime import datetime

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


def test_longform_post_has_dates(longform_post):
    rv = client.get(longform_post.url)
    assert "Published" in rv.rendered_content
    assert "Updated" not in rv.rendered_content
    longform_post.updated_at = datetime.now()
    longform_post.save_revision().publish()
    rv = client.get(longform_post.url)
    assert "First published" in rv.rendered_content
    assert "Updated" in rv.rendered_content


def test_longform_post_has_history(longform_post):
    rv = client.get(longform_post.url)
    assert "See all versions" not in rv.rendered_content
    assert "History" not in rv.rendered_content
    longform_post.history = "<h3>are doomed to repeat it<h3>"
    longform_post.save_revision().publish()
    rv = client.get(longform_post.url)
    assert "are doomed to repeat it" in rv.rendered_content
    assert "See all versions" in rv.rendered_content
    assert "History" in rv.rendered_content


def test_longform_post_gets_created(longform_post):
    """Test that we have a longform post created by the fixture
    """
    assert longform_post is not None


def test_longform_post_200(longform_post):
    """Test that we have a longform post created by the fixture
    """
    rv = client.get(longform_post.url)
    assert rv.status_code == 200
