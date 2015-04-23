# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imagestore', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='album',
            options={'verbose_name': 'Album', 'verbose_name_plural': 'Albums', 'permissions': (('moderate_albums', 'View, update and delete any album'),)},
        ),
        migrations.RemoveField(
            model_name='album',
            name='brief',
        ),
        migrations.RemoveField(
            model_name='album',
            name='created',
        ),
        migrations.RemoveField(
            model_name='album',
            name='head',
        ),
        migrations.RemoveField(
            model_name='album',
            name='is_public',
        ),
        migrations.RemoveField(
            model_name='album',
            name='name',
        ),
        migrations.RemoveField(
            model_name='album',
            name='updated',
        ),
        migrations.RemoveField(
            model_name='album',
            name='user',
        ),
        migrations.RemoveField(
            model_name='image',
            name='created',
        ),
        migrations.RemoveField(
            model_name='image',
            name='description',
        ),
        migrations.RemoveField(
            model_name='image',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='image',
            name='title',
        ),
        migrations.RemoveField(
            model_name='image',
            name='updated',
        ),
        migrations.RemoveField(
            model_name='image',
            name='user',
        ),
    ]
