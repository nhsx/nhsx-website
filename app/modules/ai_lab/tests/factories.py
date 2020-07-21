import wagtail_factories
import factory
import pytest

from modules.ai_lab.models.home_page import AiLabHomePage
from modules.ai_lab.models.resource_listings import (
    AiLabResourceIndexPage,
    AiLabUnderstandIndexPage,
    AiLabDevelopIndexPage,
    AiLabAdoptIndexPage,
)
from modules.ai_lab.models.resources import AiLabCaseStudy, AiLabExternalResource

from modules.core.tests.factories import CorePageFactory
from wagtail.core.models import Site


class AiLabHomePageFactory(CorePageFactory):
    title = "Ai Lab Home"

    @factory.lazy_attribute
    def parent(self):
        return Site.objects.all()[0].root_page

    class Meta:
        model = AiLabHomePage


class ResourceFactory(CorePageFactory):
    summary = factory.Faker("sentence")

    class Meta:
        abstract = True


class AiLabCaseStudyFactory(ResourceFactory):
    title = factory.Sequence(lambda n: "Case Study %d" % n)

    class Meta:
        model = AiLabCaseStudy


class AiLabExternalResourceFactory(ResourceFactory):
    title = factory.Sequence(lambda n: "External Resource %d" % n)
    external_url = factory.Faker("url")

    class Meta:
        model = AiLabExternalResource


class AiLabResourceIndexPageFactory(CorePageFactory):
    title = factory.Sequence(lambda n: "Case Study %d" % n)

    @factory.lazy_attribute
    def parent(self):
        return AiLabHomePageFactory.create()

    class Meta:
        model = AiLabResourceIndexPage


class AiLabCategoryIndexPageFactory(CorePageFactory):
    summary_title = "This is the summary title"
    summary_body = "This is the summary body"

    @factory.lazy_attribute
    def parent(self):
        return AiLabResourceIndexPageFactory.create()


class AiLabUnderstandIndexPageFactory(AiLabCategoryIndexPageFactory):
    title = "Resources to Understand AI"

    class Meta:
        model = AiLabUnderstandIndexPage


class AiLabDevelopIndexPageFactory(AiLabCategoryIndexPageFactory):
    title = "Resources to Develop AI"

    class Meta:
        model = AiLabDevelopIndexPage


class AiLabAdoptIndexPageFactory(AiLabCategoryIndexPageFactory):
    title = "Resources to Adopt AI"

    class Meta:
        model = AiLabAdoptIndexPage
