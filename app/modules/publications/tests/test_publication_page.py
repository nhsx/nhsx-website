import json
import re
import pytest
from django.test import Client, TestCase
from django.core.management.commands import loaddata
from modules.publications.models import PublicationPage
from datetime import datetime

pytestmark = pytest.mark.django_db
client = Client()


def test_publication_streamfield_has_anchors(publication_page):
    publication_page.body = json.dumps(
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
    publication_page.save_revision().publish()
    rv = client.get(publication_page.url)
    assert '<h2 id="a-title">' in rv.rendered_content
    assert '<h2 id="a-title-2">' in rv.rendered_content
    assert '<h2 id="a-title-3">' in rv.rendered_content
    assert '<h2 id="a-different-title">' in rv.rendered_content
    assert re.search("\<a[^>]+href='#a-title'\>", rv.rendered_content)
    assert re.search("\<a[^>]+href='#a-title-2'\>", rv.rendered_content)
    assert re.search("\<a[^>]+href='#a-title-3'\>", rv.rendered_content)
    assert re.search("\<a[^>]+href='#a-different-title'\>", rv.rendered_content)


def test_publication_page_has_dates(publication_page):
    rv = client.get(publication_page.url)
    assert "Published" in rv.rendered_content
    assert "Updated" not in rv.rendered_content
    publication_page.updated_at = datetime.now()
    publication_page.save_revision().publish()
    rv = client.get(publication_page.url)
    assert "First published" in rv.rendered_content
    assert "Updated" in rv.rendered_content


def test_publication_page_has_history(publication_page):
    rv = client.get(publication_page.url)
    assert "See updates" not in rv.rendered_content
    assert "History" not in rv.rendered_content
    publication_page.history = "<h3>are doomed to repeat it<h3>"
    publication_page.save_revision().publish()
    rv = client.get(publication_page.url)
    assert "are doomed to repeat it" in rv.rendered_content
    assert "See updates" in rv.rendered_content
    assert "History" in rv.rendered_content


def test_publication_page_gets_created(publication_page):
    """Test that we have a publication page created by the fixture
    """
    assert publication_page is not None


def test_publication_page_200(publication_page):
    """Test that we have a publication page created by the fixture
    """
    rv = client.get(publication_page.url)
    assert rv.status_code == 200
