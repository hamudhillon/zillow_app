# Generated by Django 3.0.6 on 2020-11-02 17:57

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0021_auto_20201102_2327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='rawdata',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict),
        ),
    ]
