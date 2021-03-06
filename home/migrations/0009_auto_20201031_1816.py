# Generated by Django 3.1.2 on 2020-10-31 18:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_auto_20201031_1110'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='Bedrooms',
            field=models.CharField(default=[], max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='result',
            name='Description',
            field=models.CharField(default=[], max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='result',
            name='Facts',
            field=models.CharField(default=[], max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='result',
            name='Pictures',
            field=models.CharField(default=[], max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='result',
            name='agent_broke',
            field=models.CharField(default=[], max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='result',
            name='agent_name',
            field=models.CharField(default=[], max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='result',
            name='agent_number',
            field=models.CharField(default=[], max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='result',
            name='agent_pic',
            field=models.CharField(default=[], max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='result',
            name='bathrooms',
            field=models.CharField(default=[], max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='result',
            name='home_fact',
            field=models.CharField(default=[], max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='result',
            name='list_date',
            field=models.CharField(default=[], max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='result',
            name='scraper',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='home.scraper'),
        ),
        migrations.AddField(
            model_name='result',
            name='zestimate',
            field=models.CharField(default=[], max_length=200, null=True),
        ),
    ]
