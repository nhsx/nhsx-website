from modules.core.models.abstract import BasePage
from modules.core.models.pages import SectionPage, ArticlePage
from django.db import models
from django.shortcuts import render
from wagtail.admin.edit_handlers import FieldPanel
from django import forms
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.models import Page
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

class AiLabExternalResource(AiLabResourceMixin, Page):
  external_url = models.URLField()
  content_panels = Page.content_panels + [
    FieldPanel('external_url', widget=forms.URLInput()),
    FieldPanel('use_case', widget=forms.Select())
  ]

class AiLabResourceIndexPage(RoutablePageMixin, BasePage):
  parent_page_types = ['AiLabHomePage']
  subpage_types = ['AiLabCaseStudy', 'AiLabExternalResource']
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
    ids = self._get_resource_ids_for_use_case(slug)
    children = Page.objects.filter(id__in=(ids)).specific()

    return render(request, 'ai_lab/ai_lab_resource_index_page.html', {
      'page': self,
      'children': children,
    })

  def _get_resource_ids_for_use_case(self, slug):
    ids = []
    for resource_ids_for_use_case in [self._get_ids_for_class(klass, slug) for klass in self.subpage_types]:
      for id in resource_ids_for_use_case:
        ids.append(id)

    return ids

  def _get_ids_for_class(self, klass, slug):
    return eval(klass).objects.child_of(self).filter(use_case__slug=slug).values_list('id', flat=True)
