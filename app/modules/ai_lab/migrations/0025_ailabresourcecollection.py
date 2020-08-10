# Generated by Django 3.0.4 on 2020-08-10 14:51

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import modules.ai_lab.models.resource_listings
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0030_auto_20200730_0850"),
        ("images", "0001_initial"),
        ("ai_lab", "0024_auto_20200730_0850"),
    ]

    operations = [
        migrations.CreateModel(
            name="AiLabResourceCollection",
            fields=[
                (
                    "sectionpage_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="core.SectionPage",
                    ),
                ),
                (
                    "resources",
                    wagtail.core.fields.StreamField(
                        [
                            (
                                "link",
                                wagtail.core.blocks.PageChooserBlock(
                                    label="Page",
                                    page_type=[
                                        "ai_lab.AiLabCaseStudy",
                                        "ai_lab.AiLabGuidance",
                                        "ai_lab.AiLabReport",
                                        "ai_lab.AiLabExternalResource",
                                    ],
                                    required=True,
                                ),
                            )
                        ],
                        blank=True,
                    ),
                ),
                (
                    "featured_image",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="images.NHSXImage",
                    ),
                ),
                (
                    "topics",
                    modelcluster.fields.ParentalManyToManyField(to="ai_lab.AiLabTopic"),
                ),
            ],
            options={"verbose_name": "Resource Collection",},
            bases=(
                modules.ai_lab.models.resource_listings.AiLabFilterableResourceMixin,
                "core.sectionpage",
            ),
        ),
    ]
