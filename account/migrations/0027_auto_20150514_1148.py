# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0026_auto_20150512_2018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailconfirmation',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 14, 18, 48, 45, 179000, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
