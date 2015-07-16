# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0006_auto_20150622_1211'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fabricatedcomponent',
            name='fabricated_component_for_project',
        ),
        migrations.RemoveField(
            model_name='fabricatedcomponent',
            name='fabricated_component_for_step',
        ),
        migrations.RemoveField(
            model_name='fabricatedcomponent',
            name='fabricated_component_from_project',
        ),
        migrations.DeleteModel(
            name='FabricatedComponent',
        ),
        migrations.RemoveField(
            model_name='projectfile',
            name='project_file_for_project',
        ),
        migrations.RemoveField(
            model_name='projectfile',
            name='project_file_for_step',
        ),
        migrations.DeleteModel(
            name='ProjectFile',
        ),
        migrations.RemoveField(
            model_name='projectstep',
            name='step_for_project',
        ),
        migrations.RemoveField(
            model_name='purchasedcomponent',
            name='product',
        ),
        migrations.RemoveField(
            model_name='purchasedcomponent',
            name='purchased_component_for_step',
        ),
        migrations.DeleteModel(
            name='ProjectStep',
        ),
        migrations.DeleteModel(
            name='PurchasedComponent',
        ),
    ]
