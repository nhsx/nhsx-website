import pytest
import pytz

import dateutil.parser
from django.test import Client
from modules.ai_lab.models import AiLabHomePage
from modules.ai_lab.tests.factories import AiLabHomePageFactory
from modules.blog_posts.tests.factories import BlogPostFactory

from wagtail.core.models import Page

pytestmark = pytest.mark.django_db

client = Client()


class TestAiLabHomePage:
    def test_page_can_be_created(self):
        home_page = AiLabHomePageFactory.create()
        assert isinstance(home_page, AiLabHomePage)
        assert home_page is not None

    def test_more_than_one_page_cannot_be_created(self, home_page):
        assert AiLabHomePage.can_create_at(home_page) == True

        # Create a Home Page
        AiLabHomePageFactory.create()

        # Assert that another can't be created
        assert AiLabHomePage.can_create_at(home_page) == False

    def test_three_newest_blog_posts_are_featured(self):
        first_published_at = pytz.utc.localize(
            dateutil.parser.parse("2020-01-01T00:00:00")
        )
        old_blog_posts = BlogPostFactory.create_batch(
            2, first_published_at=first_published_at, tags=["AI Lab"]
        )
        new_blog_posts = BlogPostFactory.create_batch(3, tags=["AI Lab"])

        home_page = AiLabHomePageFactory.create()

        rv = client.get(home_page.url)

        for blog_post in new_blog_posts:
            assert blog_post.title in str(rv.content)

        for blog_post in old_blog_posts:
            assert blog_post.title not in str(rv.content)
