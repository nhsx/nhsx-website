from django import forms
from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.models import Page

from modules.core.models.abstract import BasePage
from modules.core.models.pages import SectionPage, ArticlePage
from modules.blog_posts.models import BlogPost


class AiLabHomePage(SectionPage):
    subpage_types = ["AiLabResourceIndexPage", "core.ArticlePage"]
    max_count = 1

    def get_context(self, request):
        context = super().get_context(request)
        blog_posts = (
            BlogPost.objects.filter(tags__slug="ai-lab")
            .distinct()
            .order_by("-first_published_at")[:3]
        )
        context.update({"blog_posts": blog_posts})
        return context


class AiLabResourceMixin(models.Model):
    parent_page_types = [
        "AiLabUnderstandIndexPage",
        "AiLabDevelopIndexPage",
        "AiLabAdoptIndexPage",
    ]

    class Meta:
        abstract = True


class AiLabCaseStudy(AiLabResourceMixin, ArticlePage):
    pass


class AiLabExternalResource(AiLabResourceMixin, Page):
    external_url = models.URLField()
    content_panels = Page.content_panels + [
        FieldPanel("external_url", widget=forms.URLInput()),
    ]


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
    subpage_types = ["AiLabCaseStudy", "AiLabExternalResource"]
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
