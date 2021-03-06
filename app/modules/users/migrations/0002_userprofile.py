# Generated by Django 3.0.4 on 2020-04-02 08:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ("images", "0001_initial"),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "bio",
                    wagtail.core.fields.RichTextField(
                        blank=True, null=True, verbose_name="Bio"
                    ),
                ),
                (
                    "short_bio",
                    wagtail.core.fields.RichTextField(
                        blank=True, null=True, verbose_name="Short bio"
                    ),
                ),
                (
                    "photo",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="images.NHSXImage",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"abstract": False,},
        ),
    ]
