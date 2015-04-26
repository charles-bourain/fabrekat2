# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fabricator', '0002_auto_20150424_0001'),
    ]

    operations = [
        migrations.CreateModel(
            name='FabricatorType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fabricator_type', models.CharField(max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='fabricator',
            name='fabricator_tools',
        ),
        migrations.AddField(
            model_name='fabricator',
            name='fabricator_blog',
            field=models.TextField(default=1, max_length=3000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fabricator',
            name='fabricator_type',
            field=models.ForeignKey(default=1, to='fabricator.FabricatorType'),
            preserve_default=False,
        ),
    ]
