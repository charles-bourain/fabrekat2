# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('imagestore', '0001_initial'),
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectimage',
            name='project_image_for_project',
            field=models.ForeignKey(related_name='imageforproject', to='project.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='albumupload',
            name='album',
            field=models.ForeignKey(blank=True, to=settings.IMAGESTORE_ALBUM_MODEL, help_text='Select an album to add these images to. leave this empty to create a new album from the supplied title.', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='image',
            name='album',
            field=models.ForeignKey(related_name='images', verbose_name='Album', blank=True, to=settings.IMAGESTORE_ALBUM_MODEL, null=True),
            preserve_default=True,
        ),
    ]
