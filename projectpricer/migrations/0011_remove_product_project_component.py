# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projectpricer', '0010_auto_20150622_0935'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='project_component',
        ),
    ]
