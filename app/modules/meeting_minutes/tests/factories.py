import wagtail_factories
import factory
import pytest
import dateutil.parser

from modules.core.tests.factories import CorePageFactory
from modules.meeting_minutes.models import MeetingMinutes, MeetingMinutesListingPage


class MeetingMinutesFactory(CorePageFactory):
    meeting_date = dateutil.parser.parse("2020-01-01")
    start_time = dateutil.parser.parse("2020-01-01T09:00:00")
    end_time = dateutil.parser.parse("2020-01-01T12:00:00")
    venue = factory.Faker("sentence")

    class Meta:
        model = MeetingMinutes


class MeetingMinutesListingPageFactory(CorePageFactory):
    title = "Minutes"

    class Meta:
        model = MeetingMinutesListingPage
