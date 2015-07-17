# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, null=True, blank=True)),
                ('last_updated', models.DateTimeField(null=True, blank=True)),
                ('price', models.IntegerField(null=True, blank=True)),
                ('ean', models.CharField(max_length=100, null=True, editable=False, blank=True)),
                ('asin', models.CharField(max_length=100, null=True, editable=False, blank=True)),
                ('upc', models.CharField(max_length=100, null=True, editable=False, blank=True)),
                ('currency', models.CharField(max_length=20, null=True, blank=True)),
                ('url', models.URLField(max_length=10000, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
