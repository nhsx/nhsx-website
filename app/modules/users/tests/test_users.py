import pytest
from django.test import Client

pytestmark = pytest.mark.django_db

client = Client()


def test_user_gets_created(user):
    """Test that we have a user created by the fixture"""
    assert user is not None


def test_user_has_full_name(user):
    """Test that user can have a full name"""
    user.first_name = "Bruce"
    user.last_name = "Wayne"

    assert user.full_name == "Bruce Wayne"
