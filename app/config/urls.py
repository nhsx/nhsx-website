# stdlib
import os

# 3rd party
from django.urls import path
from django.conf import settings
from django.http import HttpResponse
from wagtail import views as wagtail_views
from wagtail.admin import urls as wagtailadmin_urls
from django.contrib import admin
from django.conf.urls import url, include
from wagtail.urls import WAGTAIL_FRONTEND_LOGIN_TEMPLATE, serve_pattern
from wagtail.documents import urls as wagtaildocs_urls
from wagtailcache.cache import cache_page
from django.contrib.auth import views as auth_views
from wagtail.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView

# Project
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
    server_env = os.environ.get("SERVER_ENV")
    if server_env == "production" or server_env == "development":
        return HttpResponse(PROD_ROBOTS, content_type="text/plain")
    else:
        return HttpResponse("User-agent: *\nDisallow: /", content_type="text/plain")


urlpatterns = [
    url(r"^django-admin/", admin.site.urls),
    url(r"^admin/", include(wagtailadmin_urls)),
    url(r"^documents/", include(wagtaildocs_urls)),
    url(r"^search/$", search_views.search, name="search"),
    url(r"^sitemap\.xml$", sitemap),
    url(r"^robots\.txt$", robots),
    url(
        r"^author-autocomplete/$",
        AuthorAutocomplete.as_view(),
        name="author-autocomplete",
    ),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # Add views for testing 404 page
    urlpatterns += [
        path("test-404/", TemplateView.as_view(template_name="404.html")),
    ]

urlpatterns = urlpatterns + [
    url(
        r"^_util/authenticate_with_password/(\d+)/(\d+)/$",
        wagtail_views.authenticate_with_password,
        name="wagtailcore_authenticate_with_password",
    ),
    url(
        r"^_util/login/$",
        auth_views.LoginView.as_view(template_name=WAGTAIL_FRONTEND_LOGIN_TEMPLATE),
        name="wagtailcore_login",
    ),
    # Wrap the serve function with wagtail-cache
    url(serve_pattern, cache_page(wagtail_views.serve), name="wagtail_serve"),
]
