# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publishedprojects', '0002_publishedproject_project_slug_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='publishedproject',
            old_name='project',
            new_name='project_link',
        ),
    ]
