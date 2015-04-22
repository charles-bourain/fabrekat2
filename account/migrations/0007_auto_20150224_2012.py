# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_auto_20150221_1219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailconfirmation',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 25, 4, 11, 59, 943000, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
