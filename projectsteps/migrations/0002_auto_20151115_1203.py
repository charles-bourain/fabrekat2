# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projectsteps', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectstep',
            name='project_step_video',
            field=models.URLField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='purchasedcomponent',
            name='purchased_component_name',
            field=models.CharField(max_length=300),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='purchasedcomponent',
            name='purchased_component_url_link',
            field=models.URLField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
