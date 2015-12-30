# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import designprofiles.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projectsteps', '__first__'),
        ('project', '__first__'),
        ('publishedprojects', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='DesignerWebsite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('website_url', models.URLField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DesignProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField()),
                ('location', models.CharField(max_length=30)),
                ('bio', models.CharField(max_length=5000)),
                ('profile_picture', models.ImageField(default=b'default_images/profile_image/no-photo-available-icon.jpg', upload_to=designprofiles.models.get_profile_picture_image_path)),
                ('interest', models.ManyToManyField(to='project.Catagory', null=True, blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WorkingStepOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('complete', models.BooleanField(default=False)),
                ('in_work', models.BooleanField(default=False)),
                ('project', models.ForeignKey(to='publishedprojects.PublishedProject')),
                ('steporder', models.ForeignKey(to='projectsteps.StepOrder')),
                ('user', models.ForeignKey(to='designprofiles.DesignProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='designerwebsite',
            name='designer',
            field=models.ForeignKey(to='designprofiles.DesignProfile'),
            preserve_default=True,
        ),
    ]
