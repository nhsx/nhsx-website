from django import template
from django.template.defaultfilters import time

register = template.Library()


@register.filter
def format_time(time_obj):
    if time_obj.hour == 12 and time_obj.minute == 0:
        return "midday"
    elif time_obj.hour == 0 and time_obj.minute == 0:
        return "midnight"
    elif time_obj.minute == 0:
        return time(time_obj, "gA").lower()
    else:
        return time(time_obj, "g.iA").lower()
