# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0018_auto_20150425_2019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailconfirmation',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 26, 3, 30, 42, 30000, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
