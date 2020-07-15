from django.template import Library, loader

register = Library()

@register.simple_tag()
def use_case_url(page, use_case):
    url = page.url + page.reverse_subpage('filter_by_use_case',args=[use_case.slug])
    return url
