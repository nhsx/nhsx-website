import pytest
import pytz
import json
import dateutil.parser

from django.test import Client
from modules.meeting_minutes.tests.factories import *
from modules.meeting_minutes.models import *

from wagtail.core.models import Page

pytestmark = pytest.mark.django_db

client = Client()


class TestMeetingMinutes:
    def test_minutes_can_be_created(self):
        minutes = MeetingMinutesFactory.create()
        assert isinstance(minutes, MeetingMinutes)
        assert minutes is not None

    def test_minutes_can_have_title_auto_populated(self):
        minutes = MeetingMinutesFactory.create(
            meeting_date=dateutil.parser.parse("2020-09-01")
        )

        assert minutes.title == "Tuesday  1 September 2020"

    def test_index_page_can_have_many_people(self, section_page):
        listing_page = MeetingMinutesListingPageFactory.create(parent=section_page)
        meetings = MeetingMinutesFactory.create_batch(3, parent=listing_page)

        assert len(listing_page.get_children()) == 3

        page = client.get(listing_page.url)

        assert page.status_code == 200

        for resource in meetings:
            assert resource.title in str(page.content)
