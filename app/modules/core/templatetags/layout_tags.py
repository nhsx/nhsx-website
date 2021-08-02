from django import template

register = template.Library()


@register.filter
def index(list, index):
    return list[index]


@register.filter
def column_class(resources):
    if len(resources) == 3:
        return "nhsuk-grid-column-one-third"
    if len(resources) == 2:
        return "nhsuk-grid-column-one-half"
    else:
        return "nhsuk-grid-column-full"
