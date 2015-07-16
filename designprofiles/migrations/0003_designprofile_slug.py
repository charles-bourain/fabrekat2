# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('designprofiles', '0002_designprofile_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='designprofile',
            name='slug',
            field=models.SlugField(default='chaz'),
            preserve_default=False,
        ),
    ]
