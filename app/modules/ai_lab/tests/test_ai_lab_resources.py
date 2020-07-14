import pytest

from django.test import Client
from modules.ai_lab.models import AiLabCaseStudy
from modules.ai_lab.tests.factories import AiLabCaseStudyFactory, AiLabUseCaseFactory
from wagtail.core.models import Page

pytestmark = pytest.mark.django_db

client = Client()

class TestAiLabResources():
    def test_case_study_can_be_created(self):
        case_study = AiLabCaseStudyFactory.create()
        assert isinstance(case_study, AiLabCaseStudy)
        assert case_study is not None

    def test_case_study_can_have_use_case_applied(self):
        use_case = AiLabUseCaseFactory.create(name="My Amazing Use Case")
        case_study = AiLabCaseStudyFactory.create(use_case=use_case)

        assert case_study.use_case.name == "My Amazing Use Case"

