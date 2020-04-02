# 3rd party
from consoler import console  # NOQA
from django.apps import apps
from wagtail.core.models import Page, Site, Collection
from mixer.backend.django import mixer  # NOQA
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


def fake_initial_migration():
    ContentType = apps.get_model('contenttypes.ContentType')
    Permission = apps.get_model('auth.Permission')
    Group = apps.get_model('auth.Group')
    wagtailadmin_content_type, created = ContentType.objects.get_or_create(
        app_label='wagtailadmin',
        model='admin'
    )

    # Create admin permission
    admin_permission, created = Permission.objects.get_or_create(
        content_type=wagtailadmin_content_type,
        codename='access_admin',
        name='Can access Wagtail admin'
    )

    # Assign it to Editors and Moderators groups
    for group in Group.objects.filter(name__in=['Editors', 'Moderators']):
        group.permissions.add(admin_permission)


def fake_group_collection_migration():
    ctype = ContentType.objects.filter(model='groupcollectionpermission').first()
    Permission.objects.get_or_create(
        name="Can add group collection permission",
        content_type=ctype,
        codename='add_groupcollectionpermission'
    )
    Permission.objects.get_or_create(
        name="Can change group collection permission",
        content_type=ctype,
        codename='change_groupcollectionpermission'
    )
    Permission.objects.get_or_create(
        name="Can delete group collection permission",
        content_type=ctype,
        codename='delete_groupcollectionpermission'
    )
    Permission.objects.get_or_create(
        name="Can view group collection permission",
        content_type=ctype,
        codename='view_groupcollectionpermission'
    )


def add_root_collection():
    """ id:AutoField                   1
        path:CharField                 0001
        depth:PositiveIntegerField     1
        numchild:PositiveIntegerField  5
        name:CharField                 Root
    """
    Collection.objects.get_or_create(
        path="0001",
        depth=1,
        name="Root"
    )


def setup():
    console.warn('SETTING UP')
    root = Page.objects.create(
        path='0001',
        depth=1,
        slug='root',
        title='root'
    )

    Site.objects.create(
        root_page_id=root.id,
        hostname='localhost',
        port=80,
        site_name="Test Site",
        is_default_site=True
    )

    fake_initial_migration()
    fake_group_collection_migration()
    add_root_collection()
