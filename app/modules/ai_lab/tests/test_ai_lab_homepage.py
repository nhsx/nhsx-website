import pytest
import pytz
import json

import dateutil.parser
from django.test import Client
from modules.ai_lab.models.home_page import AiLabHomePage
from modules.ai_lab.tests.factories import *
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

    def test_the_homepage_shows_resources(self):
        home_page = AiLabHomePageFactory.create()
        resource_index_page = AiLabResourceIndexPageFactory.create(parent=home_page)

        understand = AiLabUnderstandIndexPageFactory.create(parent=resource_index_page)
        develop = AiLabDevelopIndexPageFactory.create(parent=resource_index_page)
        adopt = AiLabAdoptIndexPageFactory.create(parent=resource_index_page)

        understand_case_studies = AiLabCaseStudyFactory.create_batch(
            3, parent=understand
        )
        develop_case_studies = AiLabCaseStudyFactory.create_batch(3, parent=develop)
        adopt_case_studies = AiLabCaseStudyFactory.create_batch(3, parent=develop)

        home_page.homepage_body = json.dumps(
            [
                {
                    "type": "resources_listing",
                    "value": {
                        "heading": "AI resources in health and care",
                        "description": "Here is a description",
                    },
                }
            ]
        )
        home_page.save_revision().publish()

        page = client.get(home_page.url)

        assert "<h2>AI resources in health and care</h2>" in str(page.content)
        assert "<p>Here is a description</p>" in str(page.content)

        for use_case in [understand, develop, adopt]:
            assert use_case.summary_title in str(page.content)
            assert use_case.summary_body in str(page.content)

        for resource in (
            understand_case_studies + develop_case_studies + adopt_case_studies
        ):
            assert resource.title in str(page.content)
