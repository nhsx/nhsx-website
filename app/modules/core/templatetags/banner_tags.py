# core/templatetags/banner_tags.py
from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag(takes_context=False)
def banner_excluded_urls():
    return getattr(settings, "BANNER_EXCLUDED_PAGE_URLS", [])
