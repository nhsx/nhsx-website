import pytest

from django.test import Client
from modules.ai_lab.tests.factories import AiLabTopicFactory
from modules.ai_lab.models.resources import AiLabTopic

pytestmark = pytest.mark.django_db

client = Client()


class TestAiLabTopics:
    def test_topic_gets_created(self):
        topic = AiLabTopicFactory.create()
        assert isinstance(topic, AiLabTopic)
        assert topic is not None
