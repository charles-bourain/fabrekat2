# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0005_purchasedcomponent_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchasedcomponent',
            name='product',
            field=models.ForeignKey(to='projectpricer.Product'),
            preserve_default=True,
        ),
    ]
