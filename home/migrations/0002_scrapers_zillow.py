# Generated by Django 3.1 on 2020-10-26 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Scrapers',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('list_name', models.CharField(max_length=200)),
                ('links', models.TextField(default=[], null=True)),
                ('status', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='zillow',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('data', models.TextField(default=[], null=True)),
            ],
        ),
    ]