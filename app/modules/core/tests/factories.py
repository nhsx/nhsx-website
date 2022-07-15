import wagtail_factories
import factory
import pytest

from django.utils import timezone
from wagtail import blocks

pytestmark = pytest.mark.django_db


class CorePageFactory(wagtail_factories.PageFactory):
    title = factory.Sequence(lambda n: "Page %d" % n)
    first_published_at = timezone.now()

    @factory.post_generation
    def publish(self, create, extracted, **kwargs):
        if not create:
            return
        self.save_revision().publish()
