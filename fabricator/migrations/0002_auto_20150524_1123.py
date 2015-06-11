# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fabricator', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fabricator',
            name='fabricator_type',
            field=models.ForeignKey(blank=True, to='fabricator.FabricatorType', null=True),
            preserve_default=True,
        ),
    ]
