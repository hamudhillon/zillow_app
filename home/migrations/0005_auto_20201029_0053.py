# Generated by Django 3.0.6 on 2020-10-28 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_auto_20201029_0048'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result',
            name='data',
        ),
        migrations.AddField(
            model_name='result',
            name='Address',
            field=models.CharField(default=[], max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='result',
            name='city',
            field=models.CharField(default=[], max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='result',
            name='price',
            field=models.CharField(default=[], max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='result',
            name='state',
            field=models.CharField(default=[], max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='result',
            name='title',
            field=models.CharField(default=[], max_length=200, null=True),
        ),
    ]
