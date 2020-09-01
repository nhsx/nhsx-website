from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core import fields
from wagtail.core import blocks
from wagtail.core.models import Page

from modules.core.models.abstract import BasePage, BaseIndexPage, CanonicalMixin

from modules.meeting_minutes.blocks import PersonBlock

people_blocks = [
    ("person", PersonBlock()),
]


class MeetingMinutes(Page):
    meeting_date = models.DateField(auto_now_add=False, auto_now=False)
    start_time = models.TimeField(auto_now_add=False, auto_now=False)
    end_time = models.TimeField(auto_now_add=False, auto_now=False)
    venue = models.CharField(max_length=255)
    attendees = fields.StreamField(people_blocks)
    apologies = fields.StreamField(people_blocks)
    items = fields.StreamField([("rich_text", blocks.RichTextBlock(group=" Content"))])

    content_panels = [
        FieldPanel("meeting_date"),
        FieldPanel("start_time"),
        FieldPanel("end_time"),
        FieldPanel("venue"),
        StreamFieldPanel("attendees"),
        StreamFieldPanel("apologies"),
        StreamFieldPanel("items"),
    ]

    def save(self, *args, **kwargs):
        self.title = self.meeting_date.strftime("%A %e %B %Y")
        return super().save(*args, **kwargs)


class MeetingMinutesListingPage(BaseIndexPage):
    _child_model = MeetingMinutes

    parent_page_types = ["core.SectionPage"]
    subpage_types = ["MeetingMinutes"]

