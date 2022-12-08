from django import template
from modules.home.models import HomePage

register = template.Library()

@register.simple_tag(takes_context=True)
def is_home(context):
    page = context.get('page', None)
    return isinstance(page,HomePage)
