# -*- coding: utf-8 -*-

"""
    users.service
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Service objects for doing business logic stuff outside of the models.
"""
from cacheops import cached
from consoler import console  # NOQA

# Application
from helpers.service import Service
from modules.core.service import _groups

from .models import User, UserProfile


class UserService(Service):

    """
    Service for managing Users
    """

    __model__ = User

    def enable(self, user: User):
        """Sets a random, usable password for the user to enable logging in and
        password reset forms.

        Args:
            user (User): The user you want to enable.
        """
        pw = self.manager.make_random_password()
        user.set_password(pw)
        user.save()

    def disable(self, user: User):
        """Sets an unusable password for a user, thereby removing their ability to log in or
        reset their password.

        Args:
            user (User): The user you want to disable.
        """
        user.user.set_unusable_password()
        user.save()

    def create(self, **kwargs):
        """Returns a new, saved instance of the user with hashed password.

        :param **kwargs: instance parameters
        """
        return self.__model__.objects.create_user(**kwargs)


_users = UserService()


class UserProfileService(Service):

    """
    Service for managing author profiles
    """

    __model__ = UserProfile


_user_profiles = UserProfileService()


class AuthorService(Service):

    """
    Service for managing Authors
    """

    __model__ = User

    @property
    def q(self):
        g = _groups.ensure("Authors")
        return self.__model__.objects.filter(groups__in=[g])

    def create(self, **kwargs):

        """Returns a new, saved instance of the user with hashed password.

        :param **kwargs: instance parameters
        """
        email = kwargs.pop("email")
        password = kwargs.pop("password")

        user_kwargs = {
            "first_name": kwargs.pop("first_name", None),
            "last_name": kwargs.pop("last_name", None),
        }

        user = self.__model__.objects.create_user(email, password, **user_kwargs)
        profile = _user_profiles.create(user=user, **kwargs)

        user.groups.add(_groups.authors)
        user.save()

        return profile

    @cached(timeout=60 * 60 * 24 * 30)
    def listing(self, user_id: int):
        author = self.q.values_list("first_name", "last_name", "slug").get(id=user_id)
        return {
            "full_name": f"{author[0]} {author[1]}",
            "first_name": author[0],
            "last_name": author[1],
            "slug": author[2],
        }


_authors = AuthorService()


class AuthorProfileService(Service):

    """
    Service for managing author profiles
    """

    __model__ = UserProfile


_author_profiles = AuthorProfileService()
