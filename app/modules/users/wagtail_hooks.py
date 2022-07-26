from django.conf.urls import url
from django.urls import reverse, include
from django.utils.translation import ugettext_lazy as _
from wagtail import hooks
from wagtail.admin.menu import Menu, MenuItem, SubmenuMenuItem

from .admin import urls as admin_urls

###################################################################################################
# Menus
###################################################################################################


class AuthorsSubmenu(SubmenuMenuItem):
    def is_shown(self, request):
        return request.user.has_perm("users.add_user")


class AuthorsMenu(Menu):
    def __init__(self):
        self._registered_menu_items = [
            MenuItem(
                _("Manage authors"),
                reverse("authors_admin:index"),
                classnames="icon icon-fa-users",
                order=10,
            ),
            MenuItem(
                _("Add new author"),
                reverse("authors_admin:create"),
                classnames="icon icon-fa-plus",
                order=20,
            ),
        ]
        self.construct_hook_name = None


@hooks.register("register_admin_menu_item")
def register_authors_menu_item():
    menu = AuthorsMenu()
    return AuthorsSubmenu(
        _("Authors"), menu, classnames="icon icon-fa-pencil", order=800
    )


###################################################################################################
# URLs
###################################################################################################


@hooks.register("register_admin_urls")
def register_user_admin_urls():
    return [
        url(r"^authors/", include((admin_urls, "authors"), namespace="authors_admin")),
    ]
