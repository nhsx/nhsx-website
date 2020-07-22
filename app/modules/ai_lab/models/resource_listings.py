from django.db import models
from django.shortcuts import render

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.models import Page

from modules.core.models.abstract import BasePage
from modules.core.models.pages import SectionPage, ArticlePage
from modules.blog_posts.models import BlogPost

from modules.ai_lab.models.resources import AiLabCaseStudy, AiLabExternalResource


class AiLabFilterableResourceMixin(RoutablePageMixin):
    @route(r"^$")
    @route(r"^topic/([a-z\-0-9]+)/$")
    def filter_by_topic(self, request, topic=None):
        resources = self._get_resources(topic)
        template = self.get_template(request)

        return render(request, template, {"resources": resources, "page": self})

    def _get_resources(self, topic=None):
        if topic is None:
            return self.get_children().specific()
        else:
            return self._filter_by_topic(self.get_children().specific(), topic)

    def _filter_by_topic(self, result, topic):
        return list(
            filter(
                lambda child: topic
                in child.topics.all().values_list("slug", flat=True),
                result,
            )
        )


class AiLabResourceIndexPage(AiLabFilterableResourceMixin, BasePage):
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

    def _get_resources(self, topic=None):
        resource_ids = []
        children = self.get_children().specific()

        for child in children:
            for resource in child.get_children().specific():
                resource_ids.append(resource.id)

        resources = (
            Page.objects.filter(id__in=resource_ids).specific().order_by("title")
        )

        if topic is None:
            return resources
        else:
            return self._filter_by_topic(resources, topic)


class AiLabCategoryIndexPageMixin(AiLabFilterableResourceMixin, SectionPage):
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
