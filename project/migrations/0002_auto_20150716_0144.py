# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project', '0001_initial'),
        ('publishedprojects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='inspired_from_project',
            field=models.OneToOneField(null=True, blank=True, to='publishedprojects.PublishedProject'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='project_creator',
            field=models.ForeignKey(related_name='project_creator_set', editable=False, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='revised_project',
            field=models.OneToOneField(null=True, blank=True, editable=False, to='project.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='inspiredproject',
            name='project_inspired_link',
            field=models.ForeignKey(related_name='inspired', blank=True, to='project.Project', null=True),
            preserve_default=True,
        ),
    ]
