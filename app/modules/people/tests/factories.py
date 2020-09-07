import wagtail_factories
import factory
import pytest

from modules.core.tests.factories import CorePageFactory
from modules.people.models import Person, PeopleListingPage


class PersonFactory(CorePageFactory):
    title = factory.Sequence(lambda n: "Person %d" % n)

    class Meta:
        model = Person


class PeopleListingPageFactory(CorePageFactory):
    title = "People"

    class Meta:
        model = PeopleListingPage
