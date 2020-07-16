import pytest

from django.test import Client
from modules.ai_lab.models import AiLabUseCase
from modules.ai_lab.tests.factories import AiLabUseCaseFactory
from wagtail.core.models import Page

pytestmark = pytest.mark.django_db

client = Client()


class TestAiLabUseCase:
    def test_use_case_can_be_created(self):
        use_case = AiLabUseCaseFactory.create()
        assert isinstance(use_case, AiLabUseCase)
        assert use_case is not None

    def test_use_case_gets_a_slug_generated(self):
        use_case = AiLabUseCaseFactory.create(name="Hello World!")
        assert use_case.slug == "hello-world"

    def test_use_case_has_a_unique_slug(self):
        use_cases = AiLabUseCaseFactory.create_batch(3, name="Hello World!")

        assert use_cases[0].slug == "hello-world"
        assert use_cases[1].slug == "hello-world-1"
        assert use_cases[2].slug == "hello-world-2"
