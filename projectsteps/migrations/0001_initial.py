# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import projectsteps.models


class Migration(migrations.Migration):

    dependencies = [
        ('projectpricer', '__first__'),
        ('project', '__first__'),
        ('publishedprojects', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='FabricatedComponent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fabricated_component_quantity', models.IntegerField(default=0)),
                ('fabricated_component_for_project', models.ForeignKey(related_name='base_project', blank=True, to='project.Project', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('project_file', models.FileField(upload_to=projectsteps.models.get_file_path, validators=[projectsteps.models.validate_file_extension])),
                ('project_file_for_project', models.ForeignKey(to='project.Project')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectStep',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('project_step_description', models.TextField(max_length=200, null=True, blank=True)),
                ('project_step_image', models.ImageField(null=True, upload_to=projectsteps.models.get_step_image_path, blank=True)),
                ('project_step_video', models.URLField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='PurchasedComponent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('purchased_component_name', models.CharField(max_length=300)),
                ('purchased_component_url_link', models.URLField(null=True, blank=True)),
                ('purchased_component_quantity', models.IntegerField(default=1)),
                ('product', models.ForeignKey(to='projectpricer.Product')),
                ('purchased_component_for_step', models.ForeignKey(to='projectsteps.ProjectStep')),
            ],
        ),
        migrations.CreateModel(
            name='StepOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(default=0)),
                ('step', models.ForeignKey(to='projectsteps.ProjectStep')),
                ('step_order_for_project', models.ForeignKey(blank=True, to='project.Project', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='projectfile',
            name='project_file_for_step',
            field=models.ForeignKey(to='projectsteps.ProjectStep'),
        ),
        migrations.AddField(
            model_name='fabricatedcomponent',
            name='fabricated_component_for_step',
            field=models.ForeignKey(to='projectsteps.ProjectStep'),
        ),
        migrations.AddField(
            model_name='fabricatedcomponent',
            name='fabricated_component_from_project',
            field=models.ForeignKey(related_name='component_project', blank=True, to='publishedprojects.PublishedProject', null=True),
        ),
    ]
