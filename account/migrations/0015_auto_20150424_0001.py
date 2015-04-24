# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_auto_20150325_1722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailconfirmation',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 24, 0, 1, 12, 376745, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
