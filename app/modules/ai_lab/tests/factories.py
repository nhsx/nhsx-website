import wagtail_factories
import factory
import pytest

from modules.ai_lab.models import AiLabHomePage, AiLabUseCase, AiLabCaseStudy, AiLabResourceIndexPage
from modules.core.tests.factories import CorePageFactory

class AiLabHomePageFactory(CorePageFactory):
  title = "Ai Lab Home"

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

class AiLabResourceIndexPageFactory(CorePageFactory):
  title = factory.Sequence(lambda n: 'Case Study %d' % n)
  class Meta:
    model = AiLabResourceIndexPage



