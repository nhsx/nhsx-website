import pytest
import pytz
import json

from django.test import Client
from modules.people.tests.factories import *
from modules.people.models import *

from wagtail.core.models import Page

pytestmark = pytest.mark.django_db

client = Client()


class TestPeople:
    def test_person_can_be_created(self):
        person = PersonFactory.create()
        assert isinstance(person, Person)
        assert person is not None

    def test_index_page_can_be_created(self):
        page = PeopleListingPageFactory.create()
        assert isinstance(page, PeopleListingPage)
        assert page is not None

    def test_index_page_can_have_many_people(self, section_page):
        listing_page = PeopleListingPageFactory.create(parent=section_page)
        people = PersonFactory.create_batch(3, parent=listing_page)

        assert len(listing_page.get_children()) == 3

        page = client.get(listing_page.url)

        assert page.status_code == 200

        for resource in people:
            assert resource.title in str(page.content)
