# Generated by Django 3.0.7 on 2020-09-07 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='qualifications',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
