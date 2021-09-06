# Generated by Django 3.2.7 on 2021-09-02 12:50

from django.db import migrations
from modules.migration_util import migrate_streamfield_name
class Migration(migrations.Migration):

    dependencies = [
        ('core', '0046_auto_20210902_1250'),
    ]

    operations = [
        migrate_streamfield_name(
            model_resolver = lambda apps: apps.get_model("publications.PublicationPage"),
            attributes = "body",
            old_name="grey_panel",
            new_name="card_feature",
            fields = {"label": "feature_heading"}
        )
    ]
