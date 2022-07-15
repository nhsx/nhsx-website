from os import path
from django_assets import Bundle, register
from webassets.filter import get_filter
from django.conf import settings

LIBSASS = get_filter(
    "libsass", includes=[path.join("/", "usr", "srv", "deps", "node_modules")]
)

uglify_js = get_filter("uglifyjs", extra_args=["--source-map", "-c", "-m"])

js_filters: list = []

if settings.DEBUG:
    css_filters = [LIBSASS]
else:
    css_filters = [LIBSASS, "cssmin"]

core_css_files = ["_dev/scss/screen.scss"]

admin_css_files = ["_dev/scss/admin.scss"]

core_js_files = [
    "_dev/js/lib/cookieconsent.min.js",
    "_dev/js/lib/ai_lab_resources.js",
    "_dev/js/lib/ai_lab_carousel.js",
    "_dev/js/main.js",
]

admin_js_files = ["_dev/js/admin.js"]

css_core_bundle = Bundle(
    *core_css_files,
    depends="_dev/scss/**/*.scss",
    filters=css_filters,
    output="dist/dist/css/main.min.css"
)
register("css_core", css_core_bundle)


css_admin_bundle = Bundle(
    *admin_css_files,
    depends="_dev/scss/**/*.scss",
    filters=css_filters,
    output="dist/css/admin_extra.min.css"
)

js_core_bundle = Bundle(*core_js_files, filters=[], output="dist/js/main.min.js")

js_admin_bundle = Bundle(
    *admin_js_files, filters=[], output="dist/js/admin_extra.min.js"
)


register("css_core", css_core_bundle)
register("css_admin", css_admin_bundle)

register("js_core", js_core_bundle)
register("js_admin", js_admin_bundle)
