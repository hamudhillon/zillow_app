# Generated by Django 3.0.6 on 2020-11-01 15:03

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_auto_20201101_1955'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='priceHistory',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict),
        ),
    ]
