# Generated by Django 3.0.7 on 2020-10-06 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ai_lab", "0028_auto_20201006_1029"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ailabtopic", name="name", field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name="ailabtopic",
            name="slug",
            field=models.SlugField(max_length=60, null=True, unique=True),
        ),
    ]
