from modules.core.models.abstract import BasePage
from modules.core.models.pages import SectionPage, ArticlePage
from django.db import models

class AiLabHomePage(SectionPage):
  subpage_types = ['AiLabResourceIndexPage']
  max_count = 1

class AiLabUseCase(models.Model):
  name = models.CharField(max_length=100)
  description = models.CharField(max_length=255)

  def __str__(self):
    return self.name

class AiLabResourceMixin(models.Model):
  parent_page_types = ['AiLabResourceIndexPage']
  use_case = models.ForeignKey(AiLabUseCase, on_delete=models.PROTECT)

  class Meta:
    abstract = True

class AiLabCaseStudy(AiLabResourceMixin, ArticlePage):
  pass

class AiLabResourceIndexPage(BasePage):
  parent_page_types = ['AiLabHomePage']
  subpage_types = ['AiLabCaseStudy']
  max_count = 1
