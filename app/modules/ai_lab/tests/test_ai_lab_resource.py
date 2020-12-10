import pytest
import json

from django.test import Client
from modules.ai_lab.models.resources import AiLabCaseStudy, AiLabGuidance, AiLabReport
from modules.ai_lab.models.resource_listings import AiLabResourceIndexPage
from modules.ai_lab.tests.factories import *
from wagtail.core.models import Page

pytestmark = pytest.mark.django_db

client = Client()


class TestAiLabResource:
    def test_case_study_can_be_created(self):
        case_study = AiLabCaseStudyFactory.create()
        assert isinstance(case_study, AiLabCaseStudy)
        assert case_study is not None

    def test_guidance_can_be_created(self):
        guidance = AiLabGuidanceFactory.create()
        assert isinstance(guidance, AiLabGuidance)
        assert guidance is not None

    def test_report_can_be_created(self):
        report = AiLabReportFactory.create()
        assert isinstance(report, AiLabReport)
        assert report is not None

    def test_case_study_can_have_use_case_applied(self):
        category_page = AiLabUnderstandIndexPageFactory.create()
        case_study = AiLabCaseStudyFactory.create(parent=category_page)

        assert isinstance(case_study, AiLabCaseStudy)

    def test_case_study_can_have_topics_applied(self):
        topics = AiLabTopicFactory.create_batch(2)
        case_study = AiLabCaseStudyFactory.create(topics=topics)

        assert len(case_study.topics.all()) == 2

    def test_case_study_template_shows_body(self):
        category_page = AiLabUnderstandIndexPageFactory.create()
        case_study = AiLabCaseStudyFactory.create(parent=category_page)

        page = client.get(case_study.url)

        assert page.status_code == 200

        assert case_study.title in str(page.content)

    def test_external_resource_redirects_to_external_url(self):
        category_page = AiLabUnderstandIndexPageFactory.create()
        external_resource = AiLabExternalResourceFactory.create(
            external_url="https://example.com", parent=category_page
        )

        page = client.get(external_resource.url)

        assert page.status_code == 302
        assert page.url == "https://example.com"

    def test_internal_resource_redirects_to_a_page(self):
        category_page = AiLabUnderstandIndexPageFactory.create()
        resource = AiLabCaseStudyFactory.create(parent=category_page)
        internal_resource = AiLabInternalResourceFactory.create(
            page=resource, parent=category_page
        )

        page = client.get(internal_resource.url)

        assert page.status_code == 302
        assert page.url == resource.url

    def test_case_study_shows_three_random_resources(self):
        category_page = AiLabUnderstandIndexPageFactory.create()

        case_study = AiLabCaseStudyFactory.create(parent=category_page)
        case_studies = AiLabCaseStudyFactory.create_batch(3, parent=category_page)

        page = client.get(case_study.url)

        assert page.status_code == 200

        for case_study in case_studies:
            assert case_study.title in str(page.content)
            assert case_study.title in str(page.content)

    def test_case_study_shows_live_resources_with_the_same_tag(self):
        topic1 = AiLabTopicFactory.create()
        topic2 = AiLabTopicFactory.create()
        category_page = AiLabUnderstandIndexPageFactory.create()

        case_study = AiLabCaseStudyFactory.create(
            parent=category_page, topics=[topic1, topic2]
        )

        AiLabCaseStudyFactory.create_batch(4, parent=category_page)

        live_featured_case_study = AiLabCaseStudyFactory.create(
            parent=category_page, topics=[topic1], live=True
        )
        draft_featured_case_study = AiLabCaseStudyFactory.create(
            parent=category_page, topics=[topic2], live=False
        )

        page = client.get(case_study.url)

        assert page.status_code == 200

        assert live_featured_case_study.title in str(page.content)
        assert draft_featured_case_study.title not in str(page.content)

    def test_case_study_shows_featured_resources(self):
        topic = AiLabTopicFactory.create()
        category_page = AiLabUnderstandIndexPageFactory.create()

        AiLabCaseStudyFactory.create_batch(4, parent=category_page, topics=[topic])

        featured_case_study_1 = AiLabCaseStudyFactory.create(parent=category_page)
        featured_case_study_2 = AiLabCaseStudyFactory.create(parent=category_page)

        case_study = AiLabCaseStudyFactory.create(
            parent=category_page,
            topics=[topic],
            featured_resources=json.dumps(
                [
                    {"type": "link", "value": featured_case_study_1.id,},
                    {"type": "link", "value": featured_case_study_2.id,},
                ]
            ),
        )

        page = client.get(case_study.url)

        assert page.status_code == 200

        assert featured_case_study_1.title in str(page.content)
        assert featured_case_study_2.title in str(page.content)
