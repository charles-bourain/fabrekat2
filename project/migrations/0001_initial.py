# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InspiredProject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('project_id', models.SlugField(editable=False)),
                ('project_name', models.CharField(max_length=20)),
                ('project_spotlight', models.BooleanField(default=False)),
                ('project_description', models.TextField(max_length=1000)),
                ('project_time_created', models.DateTimeField(auto_now_add=True)),
                ('project_last_modified', models.DateTimeField(auto_now=True)),
                ('project_id_from_revised_project', models.SlugField(editable=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
