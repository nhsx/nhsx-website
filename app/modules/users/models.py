# -*- coding: utf-8 -*-

"""
    modules.user.models
    ~~~~~~~~~~~~~~~~~~~
    User models.
"""

from __future__ import absolute_import, unicode_literals

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.utils.functional import cached_property
from django.contrib.auth.models import BaseUserManager
from django_extensions.db.fields import AutoSlugField
from wagtail.core import fields
from modelcluster.models import ClusterableModel


class CustomUserManager(BaseUserManager):

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('A unique email is required.')
        email = self.normalize_email(email)
        user = self.model(
            email=email, is_staff=is_staff, is_active=True, is_superuser=is_superuser,
            last_login=now, date_joined=now, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    We need a custom user model because Django wants usernames, and usernames aren't helpful.
    This custom user model is email/password only, and allows us to link to a profile model
    too.

    Email and password are required. Other fields are optional.

    Attributes:
        created_at (datetime): Date the DB record was created
        date_joined (datetime): Date the user joined
        email (str): Email address
        first_name (str): User's first name
        is_active (bool): Is this user active?
        is_staff (bool): Are they allowed to log in to the admin?
        last_name (str): User's last name
        objects (CustomUserManager): The custom user manager
        REQUIRED_FIELDS (list): Which fields are required?
        updated_at (datetime): The last updated time for this user record
        USERNAME_FIELD (str): Which field are we treating as the username?
    """
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    email = models.EmailField(_('email address'), max_length=254, unique=True)
    first_name = models.CharField(_('first name'), max_length=255, blank=True, null=True)
    last_name = models.CharField(_('last name'), max_length=255, blank=True, null=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.')
    )
    legacy_id = models.IntegerField(blank=True, null=True, unique=True)
    legacy_author_id = models.IntegerField(blank=True, null=True, unique=True)
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_('Unsetting this should be used to deactivate a user instead of deleting them.')
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True, blank=True, null=True)

    slug = AutoSlugField(
        allow_unicode=True, null=True, default=None, unique=True,
        populate_from=('first_name', 'last_name')
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        return self.full_name

    @cached_property
    def absolute_url(self):
        return "/users/%s/" % urlquote(self.email)

    @cached_property
    def full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    @cached_property
    def bio(self):
        try:
            return self.profile.bio
        except AttributeError:
            return ''

    @cached_property
    def title(self):
        """Hack to make this work with AutoCompletePanel"""
        return self.full_name

    @cached_property
    def short_name(self):
        "Returns the short name for the user."
        return self.first_name

    @property
    def has_profile(self):
        "Boolean: if user has a profile"
        try:
            self.profile
        except Exception:
            return False
        else:
            return True

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        if len(self.full_name) > 1:
            return '{} ({})'.format(self.full_name, self.email)
        else:
            return self.email


# class UserProfile(ClusterableModel):
#     """User profile model. 1to1 with the custom User model.

#     TODO Decide if we want / need all / any of these fields.

#     Attributes:
#         user (User): The user whose profile this is.
#     """

#     user = models.OneToOneField(
#         User,
#         null=True,
#         blank=True,
#         on_delete=models.SET_NULL,
#         related_name='profile'
#     )

#     city = models.CharField(_('City'), max_length=255, blank=True, null=True)
#     country = models.CharField(_('Country'), max_length=255, blank=True, null=True)
#     bio = fields.RichTextField(_('Bio'), blank=True, null=True)
#     short_bio = fields.RichTextField(_('Short bio'), blank=True, null=True)
#     photo = models.ForeignKey(
#         settings.WAGTAILIMAGES_IMAGE_MODEL,
#         null=True,
#         blank=True,
#         on_delete=models.SET_NULL,
#         related_name='+'
#     )
#     organisation = models.CharField(_('Organisation'), max_length=255, blank=True, null=True)

#     @property
#     def avatar(self):
#         """Returns the author's profile pic, or a default image"""
#         if self.photo is None:
#             return None
#         return self.photo

#     def __str__(self):
#         return self.user.full_name
