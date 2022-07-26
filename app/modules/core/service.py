from helpers.service import Service

from django.contrib.auth.models import Group
from wagtail.models import Collection, Page
from django.utils.functional import cached_property

from modules.core.models.pages import SectionPage, ArticlePage


class GroupService(Service):
    __model__ = Group

    def ensure(self, name: str) -> Group:
        """Ensures that a grouyp called ``name`` exists, and returns
        that group.

        Args:
            name (str): The name of the collection you want
        """
        try:
            group = self.get_or_create(name=name)
        except Exception:
            raise

        return group

    @cached_property
    def authors(self):
        return self.ensure("Authors")


_groups = GroupService()


class CollectionService(Service):
    __model__ = Collection

    def ensure(self, name: str) -> Collection:
        """Ensures that a collection called ``name`` exists, and returns
        that collection.

        Args:
            name (str): The name of the collection you want
        """
        try:
            coll = Collection.objects.get(name=name)
        except Collection.DoesNotExist:
            try:
                root_collection = Collection.get_first_root_node()
                coll = root_collection.add_child(name=name)
            except Exception:
                raise

        return coll


_collections = CollectionService()


class PageService(Service):
    __model__ = Page


_pages = PageService()


class SectionPageService(Service):
    __model__ = SectionPage


_sections_pages = SectionPageService()


class ArticlePageService(Service):
    __model__ = ArticlePage


_article_pages = ArticlePageService()
