import pytest
from django.test import Client


pytestmark = pytest.mark.django_db

client = Client()


def test_home_page_gets_created(home_page):
    """Test that we have a home page created by the fixture"""
    assert home_page is not None
    assert home_page.title == "Test Site Home"


def test_home_page_200(home_page):
    """Test that we have a home page created by the fixture"""
    rv = client.get(home_page.url)
    assert rv.status_code == 200
