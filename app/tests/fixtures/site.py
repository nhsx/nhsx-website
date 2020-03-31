import pytest
from wagtail.core.models import Page


@pytest.fixture(scope="function")
def site_root():
    return Page.objects.filter(path='0001').first()
