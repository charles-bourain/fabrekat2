# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projectpricer', '0002_auto_20150621_1601'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='amazon_item_id',
            new_name='upc',
        ),
    ]
