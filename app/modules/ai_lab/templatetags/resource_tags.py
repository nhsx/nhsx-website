from django import template
from django.utils.text import slugify

register = template.Library()


@register.filter
def resource_type(resource):
    return resource._meta.verbose_name


@register.filter
def link_to_resource_type(resource, page):
    slug = slugify(resource._meta.verbose_name)
    return page.url + page.reverse_subpage("filter_by_type", args=[slug])

