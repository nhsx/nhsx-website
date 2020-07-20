from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel

from modules.core.models.abstract import BasePage
from modules.core.models.pages import SectionPage, ArticlePage
from modules.blog_posts.models import BlogPost

from modules.ai_lab.models.resources import AiLabCaseStudy, AiLabExternalResource


class AiLabResourceIndexPage(BasePage):
    """
    An index page that lists all resources listed in the child
    sections
    """

    parent_page_types = ["AiLabHomePage"]
    subpage_types = [
        "AiLabUnderstandIndexPage",
        "AiLabDevelopIndexPage",
        "AiLabAdoptIndexPage",
    ]

    sub_head = models.CharField(max_length=255, blank=True, null=True)

    content_panels = [
        FieldPanel("title"),
        FieldPanel("sub_head"),
        StreamFieldPanel("body"),
    ]

    def get_context(self, request):
        context = super().get_context(request)

        resources = []
        for child in self.get_children().specific():
            for resource in child.get_children().specific():
                resources.append(resource)

        context["resources"] = sorted(resources, key=lambda r: r.title)

        return context


class AiLabCategoryIndexPageMixin(SectionPage):
    """
    A Mixin to be used by the category listing index pages
    """

    parent_page_types = ["AiLabResourceIndexPage"]
    subpage_types = [
        "AiLabCaseStudy",
        "AiLabExternalResource",
        "AiLabGuidance",
        "AiLabReport",
    ]
    max_count = 1

    summary_title = models.CharField(
        max_length=100,
        help_text="The title that will appear on the resource index page",
    )
    summary_body = models.CharField(
        max_length=255,
        help_text="The description that will appear on the resource index page",
    )

    content_panels = [
        FieldPanel("title"),
        FieldPanel("sub_head"),
        FieldPanel("summary_title"),
        FieldPanel("summary_body"),
    ]

    def get_template(self, request):
        return "ai_lab/ai_lab_category_index_page.html"

    class Meta:
        abstract = True


class AiLabUnderstandIndexPage(AiLabCategoryIndexPageMixin):
    class Meta:
        verbose_name = "Understanding AI Index Page"


class AiLabDevelopIndexPage(AiLabCategoryIndexPageMixin):
    class Meta:
        verbose_name = "Developing AI Index Page"


class AiLabAdoptIndexPage(AiLabCategoryIndexPageMixin):
    class Meta:
        verbose_name = "Adopting AI Index Page"
