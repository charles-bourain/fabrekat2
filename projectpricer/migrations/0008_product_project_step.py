# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_auto_20150621_1539'),
        ('projectpricer', '0007_product_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='project_step',
            field=models.ForeignKey(default=1, to='project.ProjectStep'),
            preserve_default=False,
        ),
    ]
