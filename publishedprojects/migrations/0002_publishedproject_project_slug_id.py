# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publishedprojects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='publishedproject',
            name='project_slug_id',
            field=models.SlugField(default=1, editable=False),
            preserve_default=False,
        ),
    ]
