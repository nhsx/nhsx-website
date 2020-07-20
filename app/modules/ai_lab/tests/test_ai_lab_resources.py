import pytest

from django.test import Client
from modules.ai_lab.models.resources import AiLabCaseStudy
from modules.ai_lab.models.resource_listings import AiLabResourceIndexPage
from modules.ai_lab.tests.factories import *
from wagtail.core.models import Page

pytestmark = pytest.mark.django_db

client = Client()


class TestAiLabResources:
    def test_case_study_can_be_created(self):
        case_study = AiLabCaseStudyFactory.create()
        assert isinstance(case_study, AiLabCaseStudy)
        assert case_study is not None

    def test_index_page_can_be_created(self):
        home_page = AiLabHomePageFactory.create()
        index_page = AiLabResourceIndexPageFactory.create(parent=home_page)
        assert isinstance(index_page, AiLabResourceIndexPage)
        assert index_page is not None

    def test_case_study_can_have_use_case_applied(self):
        category_page = AiLabUnderstandIndexPageFactory.create()
        case_study = AiLabCaseStudyFactory.create(parent=category_page)

        assert isinstance(case_study, AiLabCaseStudy)

    def test_index_page_shows_subpages(self):
        resource_index_page = AiLabResourceIndexPageFactory.create()

        understand = AiLabUnderstandIndexPageFactory.create(
            parent=resource_index_page,
            summary_title="Understanding AI",
            summary_body="Some stuff about understanding AI.",
        )
        develop = AiLabDevelopIndexPageFactory.create(
            parent=resource_index_page,
            summary_title="Developing AI",
            summary_body="Some stuff about developing AI.",
        )
        adopt = AiLabAdoptIndexPageFactory.create(
            parent=resource_index_page,
            summary_title="Adopting AI",
            summary_body="Some stuff about adopting AI.",
        )

        page = client.get(resource_index_page.url)

        assert page.status_code == 200

        for subpage in [understand, develop, adopt]:
            assert subpage.summary_title in str(page.content)
            assert subpage.summary_body in str(page.content)

    def test_index_page_lists_resources(self):
        resources_index_page = AiLabResourceIndexPageFactory.create()

        understand = AiLabUnderstandIndexPageFactory.create(parent=resources_index_page)
        develop = AiLabDevelopIndexPageFactory.create(parent=resources_index_page)
        adopt = AiLabAdoptIndexPageFactory.create(parent=resources_index_page)

        assert AiLabCaseStudy.can_create_at(understand) == True
        assert AiLabCaseStudy.can_create_at(develop) == True
        assert AiLabCaseStudy.can_create_at(adopt) == True

        understand_case_studies = AiLabCaseStudyFactory.create_batch(
            3, parent=understand
        )
        develop_case_studies = AiLabCaseStudyFactory.create_batch(3, parent=develop)
        adopt_case_studies = AiLabCaseStudyFactory.create_batch(3, parent=develop)

        understand_external_resources = AiLabExternalResourceFactory.create_batch(
            2, parent=understand
        )
        develop_external_resources = AiLabExternalResourceFactory.create_batch(
            2, parent=develop
        )

        page = client.get(resources_index_page.url)

        assert page.status_code == 200

        for resource in (
            understand_case_studies + develop_case_studies + adopt_case_studies
        ):
            assert resource.title in str(page.content)

        for resource in understand_external_resources + develop_external_resources:
            assert resource.title in str(page.content)

    def resource_index_page_shows_children(self):
        resource_index_page = AiLabUnderstandIndexPageFactory.create()

        case_studies = AiLabCaseStudyFactory.create_batch(2, parent=resource_index_page)
        external_resources = AiLabExternalResourceFactory.create_batch(
            3, parent=resource_index_page
        )

        page = client.get(resource_index_page.url)

        assert page.status_code == 200

        for resource in case_studies + external_resources:
            assert resource.title in str(page.content)
