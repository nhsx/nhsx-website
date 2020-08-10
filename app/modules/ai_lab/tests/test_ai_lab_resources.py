import pytest

from django.test import Client
from modules.ai_lab.models.resources import AiLabCaseStudy
from modules.ai_lab.models.resource_listings import AiLabResourceIndexPage
from modules.ai_lab.tests.factories import *
from wagtail.core.models import Page

pytestmark = pytest.mark.django_db

client = Client()


class TestAiLabResources:
    def test_index_page_can_be_created(self):
        home_page = AiLabHomePageFactory.create()
        index_page = AiLabResourceIndexPageFactory.create(parent=home_page)
        assert isinstance(index_page, AiLabResourceIndexPage)
        assert index_page is not None

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
            assert subpage.title in str(page.content)
            assert subpage.summary_body in str(page.content)

    def test_index_page_lists_topics(self):
        topics = AiLabTopicFactory.create_batch(7)
        index_page = AiLabResourceIndexPageFactory.create()

        page = client.get(index_page.url)

        for topic in topics:
            assert topic.name in str(page.content)

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

        resource_ids = [
            _.id
            for _ in (
                understand_case_studies
                + develop_case_studies
                + adopt_case_studies
                + understand_external_resources
                + develop_external_resources
            )
        ]
        resources = Page.objects.filter(id__in=resource_ids).order_by("title")

        for resource in resources[0:9]:
            assert resource.title in str(page.content)

        page2 = client.get(resources_index_page.url + "?page=2")

        assert page2.status_code == 200

        for resource in resources[9:]:
            assert resource.title in str(page2.content)

    def test_resource_index_page_shows_children(self):
        resource_index_page = AiLabUnderstandIndexPageFactory.create()

        case_studies = AiLabCaseStudyFactory.create_batch(2, parent=resource_index_page)
        external_resources = AiLabExternalResourceFactory.create_batch(
            3, parent=resource_index_page
        )

        page = client.get(resource_index_page.url)

        assert page.status_code == 200

        for resource in case_studies + external_resources:
            assert resource.title in str(page.content)

    def test_resource_index_page_lists_topics(self):
        topics = AiLabTopicFactory.create_batch(7)
        resource_index_page = AiLabUnderstandIndexPageFactory.create()

        page = client.get(resource_index_page.url)

        for topic in topics:
            assert topic.name in str(page.content)

    def test_resource_index_page_filters_by_topic(self):
        resource_index_page = AiLabUnderstandIndexPageFactory.create()
        topic = AiLabTopicFactory(name="Access Funding")

        case_studies = AiLabCaseStudyFactory.create_batch(
            2, parent=resource_index_page, topics=[topic]
        )
        external_resources = AiLabExternalResourceFactory.create_batch(
            3, parent=resource_index_page, topics=[topic]
        )

        other_case_studies = AiLabCaseStudyFactory.create_batch(
            2, parent=resource_index_page
        )
        other_external_resources = AiLabExternalResourceFactory.create_batch(
            3, parent=resource_index_page
        )

        url = resource_index_page.url + resource_index_page.reverse_subpage(
            "filter_by_topic", args=(topic.slug,)
        )
        page = client.get(url)

        assert page.status_code == 200

        for resource in case_studies + external_resources:
            assert resource.title in str(page.content)

        for resource in other_case_studies + other_external_resources:
            assert resource.title not in str(page.content)

    def test_resource_index_page_filters_by_type(self):
        resource_index_page = AiLabUnderstandIndexPageFactory.create()
        topic = AiLabTopicFactory(name="Access Funding")

        case_studies = [
            AiLabCaseStudyFactory.create(parent=resource_index_page),
            AiLabCaseStudyFactory.create(parent=resource_index_page, topics=[topic]),
        ]
        external_resources = AiLabExternalResourceFactory.create_batch(
            3, parent=resource_index_page
        )

        url = resource_index_page.url + resource_index_page.reverse_subpage(
            "filter_by_type", args=("case-study",)
        )
        page = client.get(url)

        assert page.status_code == 200

        for resource in case_studies:
            assert resource.title in str(page.content)

        for resource in external_resources:
            assert resource.title not in str(page.content)

        url = resource_index_page.url + resource_index_page.reverse_subpage(
            "filter_by_type", args=("case-study", topic.slug)
        )

        page2 = client.get(url)

        assert page2.status_code == 200

        assert case_studies[0].title not in str(page2.content)
        assert case_studies[1].title in str(page2.content)

    def test_index_page_filters_by_topics(self):
        index_page = AiLabResourceIndexPageFactory.create()
        parent = AiLabUnderstandIndexPageFactory.create(parent=index_page)

        topic = AiLabTopicFactory(name="Access Funding")

        case_studies = AiLabCaseStudyFactory.create_batch(
            3, topics=[topic], parent=parent
        )
        other_case_studies = AiLabCaseStudyFactory.create_batch(2, parent=parent)

        external_resources = AiLabCaseStudyFactory.create_batch(
            3, topics=[topic], parent=parent
        )
        other_external_resources = AiLabExternalResourceFactory.create_batch(
            2, parent=parent
        )

        url = index_page.url + index_page.reverse_subpage(
            "filter_by_topic", args=(topic.slug,)
        )
        page = client.get(url)

        assert page.status_code == 200

        for resource in case_studies + external_resources:
            assert resource.title in str(page.content)

        for resource in other_case_studies + other_external_resources:
            assert resource.title not in str(page.content)

    def test_index_page_filters_by_type(self):
        index_page = AiLabResourceIndexPageFactory.create()
        parent = AiLabUnderstandIndexPageFactory.create(parent=index_page)

        topic = AiLabTopicFactory(name="Access Funding")

        case_studies = [
            AiLabCaseStudyFactory.create(parent=parent),
            AiLabCaseStudyFactory.create(parent=parent, topics=[topic]),
        ]

        external_resources = AiLabExternalResourceFactory.create_batch(
            2, parent=parent, topics=[topic]
        )

        url = index_page.url + index_page.reverse_subpage(
            "filter_by_type", args=("case-study",)
        )

        page = client.get(url)

        assert page.status_code == 200

        for resource in case_studies:
            assert resource.title in str(page.content)

        for resource in external_resources:
            assert resource.title not in str(page.content)

        url = index_page.url + index_page.reverse_subpage(
            "filter_by_type", args=("case-study", topic.slug)
        )

        page2 = client.get(url)

        assert page2.status_code == 200

        assert case_studies[0].title not in str(page2.content)
        assert case_studies[1].title in str(page2.content)
