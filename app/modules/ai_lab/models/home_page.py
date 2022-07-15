from modules.core.models.pages import SectionPage, ArticlePage
from modules.blog_posts.models import BlogPost
from modules.ai_lab.blocks import ai_lab_home_page_blocks
from wagtail import fields
from wagtail.models import Page
from wagtail.admin.panels import StreamFieldPanel, FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from modules.publications.models import PublicationPage


class AiLabHomePage(SectionPage):
    subpage_types = [
        "AiLabResourceIndexPage",
        "core.ArticlePage",
        "core.SectionPage",
        "publications.PublicationPage",
    ]
    max_count = 1
    homepage_body = fields.StreamField(
        ai_lab_home_page_blocks, blank=True, verbose_name="Body blocks"
    )

    content_panels = [
        *Page.content_panels,
        FieldPanel("sub_head"),
        ImageChooserPanel("image"),
        StreamFieldPanel("homepage_body"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        blog_posts = (
            BlogPost.objects.filter(tags__slug="ai-lab")
            .live()
            .distinct()
            .order_by("-first_published_at")[:3]
        )
        context.update({"blog_posts": blog_posts})
        return context

    class Meta:
        verbose_name = "AI Lab Homepage"
