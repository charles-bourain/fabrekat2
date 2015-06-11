# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import geoposition.fields


class Migration(migrations.Migration):

    dependencies = [
        ('fabricator', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fabricator',
            name='fabricator_location',
            field=geoposition.fields.GeopositionField(default=b'47.609490406688096, -122.31884837150574', max_length=42),
            preserve_default=True,
        ),
    ]
