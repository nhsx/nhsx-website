import pytest
import json
from django.test import Client

from modules.core.models import ArticlePage
from taggit.models import Tag

from .blocks import (
    assert_rich_text,
    assert_promo,
    assert_small_promo,
)

pytestmark = pytest.mark.django_db

client = Client()


def test_article_page_gets_created(article_page):
    """Test that we have a article page created by the fixture
    """
    assert isinstance(article_page, ArticlePage)
    assert article_page is not None


def test_article_page_200(article_page):
    """Test that the article page is reachable and returns a 200
    """
    rv = client.get(article_page.url)
    assert rv.status_code == 200


def test_article_page_with_body(article_page_with_body):
    """Test that we have a article page created by the fixture
    """
    p = article_page_with_body
    assert isinstance(p, ArticlePage)
    assert p is not None
    rv = client.get(p.url)
    rendered = p.body.render_as_block()
    assert_rich_text(rendered)
    assert_promo(rendered)
    assert_small_promo(rendered)
    assert rv.status_code == 200


def test_article_page_with_latest_blog_posts(article_page, blog_posts):
    """Test that we can list blog posts with a specific tag
        when using that block"""

    p = article_page

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
