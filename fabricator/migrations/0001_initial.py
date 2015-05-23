# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import geoposition.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Fabricator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fabricator_slug', models.SlugField()),
                ('fabricator_qualifications', models.CharField(max_length=200)),
                ('fabricator_blog', models.TextField(max_length=3000)),
                ('fabricator_location', geoposition.fields.GeopositionField(max_length=42)),
                ('fabricator', models.OneToOneField(editable=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FabricatorPortfolio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('portfolio_image', models.ImageField(upload_to=b'')),
                ('fabricator', models.OneToOneField(to='fabricator.Fabricator')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
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
        migrations.AddField(
            model_name='fabricatorportfolio',
            name='fabricator_type_portfolio',
            field=models.ForeignKey(to='fabricator.FabricatorType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fabricator',
            name='fabricator_type',
            field=models.ForeignKey(to='fabricator.FabricatorType'),
            preserve_default=True,
        ),
    ]
