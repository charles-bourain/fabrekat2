# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0015_auto_20150424_0001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailconfirmation',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 24, 0, 7, 10, 980656, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
