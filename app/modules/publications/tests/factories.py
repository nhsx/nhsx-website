import wagtail_factories
import factory
import pytest
from datetime import datetime
from django.utils import timezone

from modules.blog_posts.models import BlogPost
from modules.core.tests.factories import CorePageFactory
from wagtail.core.models import Site


class PublicationFactory(CorePageFactory):
    title = factory.Faker("sentence")
    first_published_at = datetime.now(tz=timezone.utc)

    class Meta:
        model = PublicationPost

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for tag in extracted:
                self.tags.add(tag)
