# Generated by Django 3.0.6 on 2020-10-28 19:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_scrapers_zillow'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='zillow',
            new_name='results',
        ),
    ]
