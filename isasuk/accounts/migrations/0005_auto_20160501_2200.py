# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_recovery'),
    ]

    operations = [
        migrations.AlterField(
            model_name='details',
            name='end',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='details',
            name='start',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
