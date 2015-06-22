# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projectpricer', '0009_auto_20150622_0935'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='project_step',
            new_name='project_component',
        ),
    ]
