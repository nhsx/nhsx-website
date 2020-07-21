import pytest

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
