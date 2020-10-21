import pytest
import wagtail_factories

from django.test import Client

pytestmark = pytest.mark.django_db

client = Client()


class TestNHSXDocument:
    def test_download_count(self):
        document = wagtail_factories.DocumentFactory.create()

        assert document.download_count == 0

        client.get(document.url)

        document.refresh_from_db()

        assert document.download_count == 1
