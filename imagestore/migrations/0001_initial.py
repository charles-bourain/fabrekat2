# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields
import imagestore.utils
import project.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.IntegerField(default=0, verbose_name='Order')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Album',
                'swappable': 'IMAGESTORE_ALBUM_MODEL',
                'verbose_name_plural': 'Albums',
                'permissions': (('moderate_albums', 'View, update and delete any album'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.IntegerField(default=0, verbose_name='Order')),
                ('image', sorl.thumbnail.fields.ImageField(upload_to=imagestore.utils.FilePathGenerator(to='imagestore/'), max_length=255, verbose_name='File')),
            ],
            options={
                'ordering': ('order', 'id'),
                'abstract': False,
                'verbose_name_plural': 'Images',
                'verbose_name': 'Image',
                'swappable': 'IMAGESTORE_IMAGE_MODEL',
                'permissions': (('moderate_images', 'View, update and delete any image'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AlbumUpload',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('zip_file', models.FileField(help_text='Select a .zip file of images to upload into a new Gallery.', upload_to='temp/', verbose_name='images file (.zip)')),
                ('new_album_name', models.CharField(help_text='If not empty new album with this name will be created and images will be upload to this album', max_length=255, verbose_name='New album name', blank=True)),
                ('tags', models.CharField(max_length=255, verbose_name='tags', blank=True)),
            ],
            options={
                'verbose_name': 'Album upload',
                'verbose_name_plural': 'Album uploads',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.IntegerField(default=0, verbose_name='Order')),
                ('image', models.ImageField(null=True, upload_to=project.models.get_image_path, blank=True)),
            ],
            options={
                'abstract': False,
                'permissions': (('moderate_albums', 'View, update and delete any album'),),
            },
            bases=(models.Model,),
        ),
    ]
