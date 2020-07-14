from modules.core.models.abstract import BasePage
from modules.core.models.pages import SectionPage, ArticlePage
from django.db import models
from wagtail.admin.edit_handlers import FieldPanel
from django import forms
from django.utils.text import slugify

class AiLabHomePage(SectionPage):
  subpage_types = ['AiLabResourceIndexPage', 'core.ArticlePage']
  max_count = 1

class AiLabUseCase(models.Model):
  name = models.CharField(max_length=100)
  description = models.CharField(max_length=255)
  slug = models.SlugField(max_length=200, null=True, unique=True)

  def save(self, *args, **kwargs):
    if not self.slug:
        self.slug = slugify(self.name)
    return super().save(*args, **kwargs)

  def __str__(self):
    return self.name

class AiLabResourceMixin(models.Model):
  parent_page_types = ['AiLabResourceIndexPage']
  use_case = models.ForeignKey(AiLabUseCase, on_delete=models.PROTECT)
  content_panels = ArticlePage.content_panels + [
    FieldPanel('use_case', widget=forms.Select())
  ]

  class Meta:
    abstract = True

class AiLabCaseStudy(AiLabResourceMixin, ArticlePage):
  pass

class AiLabResourceIndexPage(BasePage):
  parent_page_types = ['AiLabHomePage']
  subpage_types = ['AiLabCaseStudy']
  max_count = 1
