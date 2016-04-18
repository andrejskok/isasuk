# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0003_group_end'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='end',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='group',
            name='start',
            field=models.CharField(max_length=50),
        ),
    ]
