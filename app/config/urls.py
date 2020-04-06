import os
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.contrib.sitemaps.views import sitemap

from modules.search import views as search_views
from modules.core.views import AuthorAutocomplete


PROD_ROBOTS = """
User-agent: *
Disallow: /admin/

User-agent: *
Allow: /

Sitemap: https://nhsx.nhs.uk/sitemap.xml
"""


def robots(request):
    server_env = os.environ.get('SERVER_ENV')
    if server_env == 'production' or server_env == 'development':
        return HttpResponse(PROD_ROBOTS, content_type="text/plain")
    else:
        return HttpResponse(
            "User-agent: *\nDisallow: /", content_type="text/plain")


urlpatterns = [
    url(r'^django-admin/', admin.site.urls),
    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),
    url(r'^search/$', search_views.search, name='search'),
    url(r'^sitemap\.xml$', sitemap),
    url(r'^robots\.txt$', robots),
    url(
        r'^author-autocomplete/$',
        AuthorAutocomplete.as_view(),
        name='author-autocomplete',
    ),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    url(r"", include(wagtail_urls)),

    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    url(r"^pages/", include(wagtail_urls)),
]
