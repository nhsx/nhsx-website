from modules.core.models.pages import SectionPage, ArticlePage
from django.db import models

class AiLabHomePage(SectionPage):
  max_count = 1

class AiLabUseCase(models.Model):
  name = models.CharField(max_length=100)
  description = models.CharField(max_length=255)

  def __str__(self):
    return self.name

class AiLabResourceMixin(models.Model):
  use_case = models.ForeignKey(AiLabUseCase, on_delete=models.PROTECT)

  class Meta:
    abstract = True

class AiLabCaseStudy(ArticlePage, AiLabResourceMixin):
  pass
