from django import template
from django.utils.text import slugify
from django.utils.html import mark_safe

register = template.Library()


@register.filter
def resource_type(resource):
    if resource._meta.verbose_name != "Internal Resource":
        return mark_safe(
            '<p class="nhsai_resource__type">' + resource._meta.verbose_name + "</p>"
        )
    else:
        return ""


@register.filter
def link_to_resource_type(resource, page):
    slug = slugify(resource._meta.verbose_name)
    return page.url + page.reverse_subpage("filter_by_type", args=[slug])


@register.filter
def ordered_subcategories(page):
    children = page.get_children().specific()

    return [
        filter_by_type(children, "AiLabUnderstandIndexPage"),
        filter_by_type(children, "AiLabDevelopIndexPage"),
        filter_by_type(children, "AiLabAdoptIndexPage"),
    ]


def filter_by_type(children, type):
    filtered_list = list([c for c in children if c.__class__.__name__ == type])
    return filtered_list[0] if filtered_list else None
