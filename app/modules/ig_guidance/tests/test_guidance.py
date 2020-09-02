import pytest
import pytz
import json
import dateutil.parser

from django.test import Client
from modules.ig_guidance.tests.factories import *
from modules.ig_guidance.models import *

from wagtail.core.models import Page

pytestmark = pytest.mark.django_db

client = Client()


class TestGuidance:
    def test_internal_guidance_can_be_created(self):
        guidance = InternalGuidanceFactory.create(topic=IGGuidanceTopicFactory.create())
        assert isinstance(guidance, InternalGuidance)
        assert guidance is not None

    def test_external_guidance_can_be_created(self):
        guidance = ExternalGuidanceFactory.create(topic=IGGuidanceTopicFactory.create())
        assert isinstance(guidance, ExternalGuidance)
        assert guidance is not None

    def test_external_guidance_redirects(self, section_page):
        index_page = GuidanceListingPageFactory.create(parent=section_page)
        guidance = ExternalGuidanceFactory.create(
            external_url="https://example.com",
            topic=IGGuidanceTopicFactory.create(),
            parent=index_page,
        )

        page = client.get(guidance.url)

        assert page.status_code == 302
        assert page.url == "https://example.com"

    def test_listing_page_lists_guidance(self, section_page):
        listing_page = GuidanceListingPageFactory.create(parent=section_page)

        internal_guidance = InternalGuidanceFactory.create_batch(
            4, topic=IGGuidanceTopicFactory.create(), parent=listing_page
        )
        external_guidance = ExternalGuidanceFactory.create_batch(
            4, topic=IGGuidanceTopicFactory.create(), parent=listing_page
        )

        page = client.get(listing_page.url)

        for guidance in internal_guidance + external_guidance:
            assert guidance.title in str(page.content)

    def test_listing_page_can_filter_by_tag(self, section_page):
        listing_page = GuidanceListingPageFactory.create(parent=section_page)
        tag = IGGuidanceTagFactory.create(name="My Amazing Tag")

        untaggged_internal_guidance = InternalGuidanceFactory.create_batch(
            1, topic=IGGuidanceTopicFactory.create(), parent=listing_page
        )

        untagged_external_guidance = ExternalGuidanceFactory.create_batch(
            2, topic=IGGuidanceTopicFactory.create(), parent=listing_page
        )

        taggged_internal_guidance = InternalGuidanceFactory.create_batch(
            2, topic=IGGuidanceTopicFactory.create(), tags=[tag], parent=listing_page
        )

        tagged_external_guidance = ExternalGuidanceFactory.create_batch(
            3, topic=IGGuidanceTopicFactory.create(), tags=[tag], parent=listing_page
        )

        url = listing_page.url + listing_page.reverse_subpage(
            "filter_by_tag", args=(tag.slug,)
        )

        page = client.get(url)

        for guidance in untaggged_internal_guidance + untagged_external_guidance:
            assert guidance.title not in str(page.content)

        for guidance in taggged_internal_guidance + tagged_external_guidance:
            assert guidance.title in str(page.content)
