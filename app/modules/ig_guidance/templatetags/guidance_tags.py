from django import template

register = template.Library()


@register.filter
def guidance_type(guidance):
    return guidance._meta.verbose_name


@register.filter
def guidance_target(guidance):
    if guidance.__class__.__name__ == "ExternalGuidance":
        return "_blank"
    else:
        return "_self"


@register.filter
def guidance_tag_url(page, tag):
    return page.url + page.reverse_subpage("filter_by_tag", args=(tag.slug,))

@register.filter
def guidance_tag(tag, current_tag):
    if tag.slug == current_tag:
        return "tag current"
    else:
        return "tag"
