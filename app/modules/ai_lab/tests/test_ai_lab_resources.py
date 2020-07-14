import pytest

from django.test import Client
from modules.ai_lab.models import AiLabCaseStudy, AiLabResourceIndexPage
from modules.ai_lab.tests.factories import AiLabCaseStudyFactory, AiLabUseCaseFactory, AiLabResourceIndexPageFactory, AiLabHomePageFactory
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

    def test_index_page_can_be_created(self):
        home_page = AiLabHomePageFactory.create()
        index_page = AiLabResourceIndexPageFactory.create(parent=home_page)
        assert isinstance(index_page, AiLabResourceIndexPage)
        assert index_page is not None

    def test_index_page_lists_subpages(self):
        resource_index_page = AiLabResourceIndexPageFactory.create()

        assert AiLabCaseStudy.can_create_at(resource_index_page) == True

        case_studies = AiLabCaseStudyFactory.create_batch(10, parent=resource_index_page)

        assert len(resource_index_page.get_children()) == len(case_studies)

        page = client.get(resource_index_page.url)

        assert page.status_code == 200

        for case_study in case_studies:
            assert case_study.title in str(page.content)

    def test_index_page_filters_by_use_case(self):
        resource_index_page = AiLabResourceIndexPageFactory.create()
        use_case = AiLabUseCaseFactory.create(name="my use case")
        case_studies = AiLabCaseStudyFactory.create_batch(5, parent=resource_index_page, use_case=use_case)
        other_case_studies = AiLabCaseStudyFactory.create_batch(2, parent=resource_index_page)

        page = client.get(resource_index_page.url + resource_index_page.reverse_subpage('filter_by_use_case', args=("my-use-case", )))

        assert page.status_code == 200

        for case_study in case_studies:
            assert case_study.title in str(page.content)

        for case_study in other_case_studies:
            assert case_study.title not in str(page.content)



