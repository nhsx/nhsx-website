import wagtail_factories
import factory
import pytest

from modules.core.tests.factories import CorePageFactory
from modules.case_studies.models import CaseStudy


class CaseStudyFactory(CorePageFactory):
    title = factory.Sequence(lambda n: "CaseStudy %d" % n)
    display_order = 0

    class Meta:
        model = CaseStudy
