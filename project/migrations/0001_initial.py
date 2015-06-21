# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import project.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('publishedprojects', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='FabricatedComponent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fabricated_component_quantity', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
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
                ('inspired_from_project', models.OneToOneField(null=True, blank=True, to='publishedprojects.PublishedProject')),
                ('project_creator', models.ForeignKey(related_name='project_creator_set', editable=False, to=settings.AUTH_USER_MODEL)),
                ('revised_project', models.OneToOneField(null=True, blank=True, editable=False, to='project.Project')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('project_file', models.FileField(upload_to=project.models.get_file_path, validators=[project.models.validate_file_extension])),
                ('project_file_for_project', models.ForeignKey(blank=True, to='project.Project', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectStep',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('project_step_description', models.TextField(max_length=200)),
                ('project_step_image', models.ImageField(null=True, upload_to=project.models.image_upload_path, blank=True)),
                ('step_order', models.IntegerField()),
                ('step_for_project', models.ForeignKey(related_name='project_step', to='project.Project')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PurchasedComponent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('purchased_component_name', models.CharField(max_length=20)),
                ('purchased_component_url_link', models.URLField()),
                ('purchased_component_quantity', models.IntegerField(default=0)),
                ('purchased_component_price', models.IntegerField(default=None, null=True)),
                ('purchased_component_for_project', models.ForeignKey(blank=True, to='project.Project', null=True)),
                ('purchased_component_for_step', models.ForeignKey(to='project.ProjectStep')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='projectfile',
            name='project_file_for_step',
            field=models.ForeignKey(to='project.ProjectStep'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='inspiredproject',
            name='project_inspired_link',
            field=models.ForeignKey(related_name='inspired', blank=True, to='project.Project', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fabricatedcomponent',
            name='fabricated_component_for_project',
            field=models.ForeignKey(related_name='base_project', blank=True, to='project.Project', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fabricatedcomponent',
            name='fabricated_component_for_step',
            field=models.ForeignKey(to='project.ProjectStep'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fabricatedcomponent',
            name='fabricated_component_from_project',
            field=models.ForeignKey(related_name='component_project', blank=True, to='publishedprojects.PublishedProject', null=True),
            preserve_default=True,
        ),
    ]
