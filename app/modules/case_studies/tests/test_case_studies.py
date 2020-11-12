import pytest
import pytz
import json

from django.test import Client
from modules.case_studies.tests.factories import *
from modules.case_studies.models import *

from wagtail.core.models import Page

pytestmark = pytest.mark.django_db

client = Client()


class TestCaseStudy:
    def test_case_study_can_be_created(self):
        casestudy = CaseStudyFactory.create()
        assert isinstance(casestudy, CaseStudyPage)
        assert casestudy is not None
