# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchasedcomponent',
            name='purchased_component_price',
            field=models.IntegerField(default=None, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='purchasedcomponent',
            name='purchased_component_quantity',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='purchasedcomponent',
            name='purchased_component_url_link',
            field=models.URLField(max_length=10000, null=True, blank=True),
            preserve_default=True,
        ),
    ]
