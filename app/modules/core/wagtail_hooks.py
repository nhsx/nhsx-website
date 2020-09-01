from wagtail.core import hooks
from cacheops import invalidate_all
from wagtailcache.cache import clear_cache
from django.templatetags.static import static
from django.utils.html import format_html


@hooks.register("after_create_page")
@hooks.register("after_edit_page")
def clear_wagtailcache(request, page):
    invalidate_all()
    if page.live:
        clear_cache()


@hooks.register("insert_global_admin_js", order=100)
def global_admin_js():
    """Add /static/js/admin_extra.min.js to the admin."""
    return format_html('<script src="{}"></script>', static("/js/admin_extra.min.js"))
