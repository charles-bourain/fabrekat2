# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('designprofiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='designprofile',
            name='location',
            field=models.CharField(default='Seattle', max_length=50),
            preserve_default=False,
        ),
    ]
