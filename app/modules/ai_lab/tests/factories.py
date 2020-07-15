import wagtail_factories
import factory
import pytest

from modules.ai_lab.models import AiLabHomePage, AiLabUseCase, AiLabCaseStudy, AiLabResourceIndexPage, AiLabExternalResource
from modules.core.tests.factories import CorePageFactory
from wagtail.core.models import Site

class AiLabHomePageFactory(CorePageFactory):
  title = "Ai Lab Home"

  @factory.lazy_attribute
  def parent(self):
      return Site.objects.all()[0].root_page

  class Meta:
    model = AiLabHomePage

class AiLabUseCaseFactory(factory.django.DjangoModelFactory):
  name = factory.Faker('word')
  description = factory.Faker('sentence')

  class Meta:
    model = AiLabUseCase

class AiLabCaseStudyFactory(CorePageFactory):
  title = factory.Sequence(lambda n: 'Case Study %d' % n)
  use_case = factory.SubFactory(AiLabUseCaseFactory)

  class Meta:
    model = AiLabCaseStudy

class AiLabExternalResourceFactory(CorePageFactory):
  title = factory.Sequence(lambda n: 'External Resource %d' % n)
  use_case = factory.SubFactory(AiLabUseCaseFactory)
  external_url = factory.Faker('url')

  class Meta:
    model = AiLabExternalResource

class AiLabResourceIndexPageFactory(CorePageFactory):
  title = factory.Sequence(lambda n: 'Case Study %d' % n)

  @factory.lazy_attribute
  def parent(self):
      return AiLabHomePageFactory.create()

  class Meta:
    model = AiLabResourceIndexPage



