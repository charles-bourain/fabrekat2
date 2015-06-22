# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projectpricer', '0008_product_project_step'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='project_step',
            field=models.ForeignKey(to='project.PurchasedComponent'),
            preserve_default=True,
        ),
    ]
