# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projectpricer', '0005_auto_20150621_1816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='asin',
            field=models.CharField(max_length=100, null=True, editable=False, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='currency',
            field=models.CharField(max_length=20, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='ean',
            field=models.CharField(max_length=100, null=True, editable=False, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='upc',
            field=models.CharField(max_length=100, null=True, editable=False, blank=True),
            preserve_default=True,
        ),
    ]
