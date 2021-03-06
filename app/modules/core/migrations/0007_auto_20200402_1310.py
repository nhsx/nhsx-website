# Generated by Django 3.0.4 on 2020-04-02 13:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("images", "0001_initial"),
        (
            "core",
            "0006_analyticssettings_defaultimagesettings_metatagsettings_socialmediasettings",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="socialmediasettings",
            name="facebook_app_id",
            field=models.URLField(
                blank=True, help_text="Your Facebook app ID if you have one", null=True
            ),
        ),
        migrations.AlterField(
            model_name="metatagsettings",
            name="description",
            field=models.TextField(
                blank=True,
                help_text="Fallback description if there isn't one set on the page",
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="metatagsettings",
            name="image",
            field=models.ForeignKey(
                blank=True,
                help_text="A fallback image to use when shared on Facebook and Twitter (aim for 1200x630)",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.NHSXImage",
            ),
        ),
    ]
