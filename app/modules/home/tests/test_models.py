import pytest

from modules.home.models import HomePage


def test_home_page_can_be_created():
    homepage = HomePage.objects.create(title="Hello", path="/", depth=1)

    assert homepage.title == "Hello"
    assert homepage.path == "/"
    assert homepage.depth == 1
