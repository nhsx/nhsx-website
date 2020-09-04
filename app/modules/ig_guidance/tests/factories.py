import wagtail_factories
import factory
import pytest
import dateutil.parser

from modules.core.tests.factories import CorePageFactory
from modules.ig_guidance.models import (
    InternalGuidance,
    ExternalGuidance,
    GuidanceListingPage,
    IGGuidanceTopic,
    IGGuidanceTag,
    IGTemplate,
)


class IGGuidanceTopicFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("word")

    class Meta:
        model = IGGuidanceTopic


class IGGuidanceTagFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("word")

    class Meta:
        model = IGGuidanceTag


class GuidanceFactory(CorePageFactory):
    summary = factory.Faker("sentence")

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            tags = extracted
        else:
            tags = IGGuidanceTagFactory.create_batch(3)

        for tag in tags:
            self.tags.add(tag)

    class Meta:
        abstract = True


class InternalGuidanceFactory(GuidanceFactory):
    class Meta:
        model = InternalGuidance


class ExternalGuidanceFactory(GuidanceFactory):
    external_url = factory.Faker("url")

    class Meta:
        model = ExternalGuidance


class IGTemplateFactory(GuidanceFactory):
    class Meta:
        model = IGTemplate


class GuidanceListingPageFactory(CorePageFactory):
    title = "Guidance"

    class Meta:
        model = GuidanceListingPage
