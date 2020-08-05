from django import forms

from wagtail.core import blocks
from modules.core.blocks import section_page_blocks


class ResourcesBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=True)
    description = blocks.CharBlock(required=False)

    def get_context(self, value, parent_context=None):
        from modules.ai_lab.models import (
            AiLabUnderstandIndexPage,
            AiLabDevelopIndexPage,
            AiLabAdoptIndexPage,
        )

        context = super().get_context(value, parent_context=parent_context)
        resource_types = [
            AiLabUnderstandIndexPage,
            AiLabDevelopIndexPage,
            AiLabAdoptIndexPage,
        ]

        resources = {}

        for type in resource_types:
            page = type.objects.all()[0]
            child_resources = page.get_children().live()[:9]
            resources[page] = child_resources

        context.update({"resources": resources})

        return context

    class Meta:
        icon = "pick"
        template = "ai_lab/blocks/resources.html"


ai_lab_home_page_blocks = section_page_blocks + [
    ("resources_listing", ResourcesBlock(group=" Content")),
]

resource_link_blocks = [
    (
        "link",
        blocks.PageChooserBlock(
            required=True,
            label="Page",
            page_type=[
                "ai_lab.AiLabCaseStudy",
                "ai_lab.AiLabGuidance",
                "ai_lab.AiLabReport",
                "ai_lab.AiLabExternalResource",
            ],
        ),
    ),
]
