import wagtail_factories
import factory
import pytest

from modules.ai_lab.models import AiLabHomePage, AiLabUseCase
from modules.core.tests.factories import CorePageFactory

class AiLabHomePageFactory(CorePageFactory):
  title = "Ai Lab Home"

  class Meta:
    model = AiLabHomePage

class AiLabUseCaseFactory(factory.Factory):
  name = factory.Faker('word')
  description = factory.Faker('sentence')

  class Meta:
    model = AiLabUseCase

