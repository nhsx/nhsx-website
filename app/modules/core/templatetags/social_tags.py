from django import template
from modules.core.models import MetaTagSettings


register = template.Library()


@register.filter(name="fb_og_description")
def fb_og_description(page, site):
    if hasattr(page, "fb_og_description") and page.fb_og_description is not None:
        return page.fb_og_description
    else:
        return MetaTagSettings.for_site(site).description


@register.filter(name="fb_image")
def fb_image(page, site):
    if hasattr(page, "fb_og_image") and page.fb_og_image is not None:
        return page.fb_og_image
    else:
        return MetaTagSettings.for_site(site).image


@register.filter(name="twitter_card_description")
def twitter_card_description(page, site):
    if (
        hasattr(page, "twitter_card_description")
        and page.twitter_card_description is not None
    ):
        return page.twitter_card_description
    else:
        return MetaTagSettings.for_site(site).description


@register.filter(name="twitter_card_image")
def twitter_card_image(page, site):
    if hasattr(page, "twitter_card_image") and page.twitter_card_image is not None:
        return page.twitter_card_image
    else:
        return MetaTagSettings.for_site(site).image


@register.filter(name="social_tag_url")
def social_tag_url(page, image):
    if image.url.startswith("http"):
        return image.url
    else:
        return page.get_site().root_url + image.url

