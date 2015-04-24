# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import project.models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '__first__'),
        ('imagestore', '0002_auto_20150325_1722'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.IntegerField(default=0, verbose_name='Order')),
                ('image', models.ImageField(null=True, upload_to=project.models.get_image_path, blank=True)),
                ('project_image_for_project', models.ForeignKey(related_name='imageforproject', to='project.Project')),
            ],
            options={
                'abstract': False,
                'permissions': (('moderate_albums', 'View, update and delete any album'),),
            },
            bases=(models.Model,),
        ),
    ]
