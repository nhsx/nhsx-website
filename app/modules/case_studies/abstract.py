# 3rd party
from django.db import models
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TagBase, ItemBase


class CaseStudyTag(TagBase):
    class Meta:
        verbose_name = "case study tag"
        verbose_name_plural = "case study tags"


class CaseStudyTags(ItemBase):
    tag = models.ForeignKey(
        CaseStudyTag, related_name="tagged_case_studies", on_delete=models.CASCADE
    )
    content_object = ParentalKey(
        to="case_studies.CaseStudyPage",
        on_delete=models.CASCADE,
        related_name="tagged_items",
    )
