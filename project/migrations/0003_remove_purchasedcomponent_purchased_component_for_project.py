# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_auto_20150621_1539'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchasedcomponent',
            name='purchased_component_for_project',
        ),
    ]
