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
