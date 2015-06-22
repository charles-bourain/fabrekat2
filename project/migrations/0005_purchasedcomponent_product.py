# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projectpricer', '0011_remove_product_project_component'),
        ('project', '0004_remove_purchasedcomponent_purchased_component_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchasedcomponent',
            name='product',
            field=models.OneToOneField(default=1, to='projectpricer.Product'),
            preserve_default=False,
        ),
    ]
