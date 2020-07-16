import wagtail_factories
import factory
import pytest

from modules.ai_lab.models import AiLabHomePage
from modules.core.tests.factories import CorePageFactory

class AiLabHomePageFactory(CorePageFactory):
  title = "Ai Lab Home"

  class Meta:
    model = AiLabHomePage
