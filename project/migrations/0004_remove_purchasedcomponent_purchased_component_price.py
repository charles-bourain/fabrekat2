# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_remove_purchasedcomponent_purchased_component_for_project'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchasedcomponent',
            name='purchased_component_price',
        ),
    ]
