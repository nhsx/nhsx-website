from django import template

register = template.Library()


@register.filter
def resource_type(resource):
    return resource._meta.verbose_name
