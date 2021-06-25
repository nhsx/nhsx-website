from wagtail.utils.decorators import cached_classmethod

# Project
from modules.core.models.abstract import BasePage, HeroImageContentMixin


class HomePage(BasePage, HeroImageContentMixin):

    hero_panels = HeroImageContentMixin.hero_panels

    subpage_types: list = [
        "core.SectionPage",
        "core.ArticlePage",
        "blog_posts.BlogPostIndexPage",
        "publications.PublicationPage",
        "news.NewsIndexPage",
        "ai_lab.AiLabHomePage",
    ]

    @cached_classmethod
    def get_admin_tabs(cls):
        tabs = super().get_admin_tabs()
        tabs.insert(1, (cls.hero_panels, "Hero"))
        return tabs

    @classmethod
    def can_create_at(cls, parent):
        """This stops admin users from creating more than one HomePage."""
        return super().can_create_at(parent) and not cls.objects.exists()
