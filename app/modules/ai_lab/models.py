from modules.core.models.abstract import BasePage
from modules.core.models.pages import SectionPage, ArticlePage
from django.db import models
from django.shortcuts import render
from wagtail.admin.edit_handlers import FieldPanel
from django import forms
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
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

class AiLabResourceIndexPage(RoutablePageMixin, BasePage):
  parent_page_types = ['AiLabHomePage']
  subpage_types = ['AiLabCaseStudy']
  max_count = 1

  @route(r'^$')
  def all_resources(self, request):
    children = self.get_children().specific()

    return render(request, 'ai_lab/ai_lab_resource_index_page.html', {
      'page': self,
      'children': children,
    })

  @route(r'^([a-z0-9]+(?:-[a-z0-9]+)*)/$')
  def filter_by_use_case(self, request, slug):
    children = AiLabCaseStudy.objects.filter(use_case__slug=slug)

    return render(request, 'ai_lab/ai_lab_resource_index_page.html', {
      'page': self,
      'children': children,
    })

