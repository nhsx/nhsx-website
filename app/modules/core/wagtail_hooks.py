
from wagtail.core import hooks
from cacheops import invalidate_all
from wagtailcache.cache import clear_cache


@hooks.register('after_create_page')
@hooks.register('after_edit_page')
def clear_wagtailcache(request, page):
    invalidate_all()
    if page.live:
        clear_cache()
