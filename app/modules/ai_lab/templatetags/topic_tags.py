from django import template

register = template.Library()


@register.filter
def topic_class(topic, current_topic):
    if topic.slug == current_topic:
        return "tag current"
    else:
        return "tag"


@register.filter
def topic_url(page, topic):
    return page.url + page.reverse_subpage("filter_by_topic", args=(topic.slug,))
