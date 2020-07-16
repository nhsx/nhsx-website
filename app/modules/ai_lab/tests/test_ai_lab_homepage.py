import pytest

from django.test import Client
from modules.ai_lab.models import AiLabHomePage
from modules.ai_lab.tests.factories import AiLabHomePageFactory
from wagtail.core.models import Page

pytestmark = pytest.mark.django_db

client = Client()

class TestAiLabHomePage():
    def test_page_can_be_created(self):
        home_page = AiLabHomePageFactory.create()
        assert isinstance(home_page, AiLabHomePage)
        assert home_page is not None

    def test_more_than_one_page_cannot_be_created(self, home_page):
        assert AiLabHomePage.can_create_at(home_page) == True

        # Create a Home Page
        AiLabHomePageFactory.create()

        # Assert that another can't be created
        assert AiLabHomePage.can_create_at(home_page) == False

