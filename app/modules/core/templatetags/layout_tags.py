from django import template

register = template.Library()


@register.filter
def index(list, index):
    try:
        return list[index]
    except TypeError:  # might not be a list, might be None
        return None
    except IndexError:  # list might be too short
        return None


@register.filter
def column_class(resources):
    if len(resources) == 3:
        return "nhsuk-grid-column-one-third"
    if len(resources) == 2:
        return "nhsuk-grid-column-one-half"
    else:
        return "nhsuk-grid-column-full"
