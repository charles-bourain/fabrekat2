# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PublishedProject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('project_slug_id', models.SlugField(editable=False)),
                ('project_link', models.OneToOneField(editable=False, to='project.Project')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
