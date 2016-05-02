# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meeting', '0008_invited'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='title',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='creator',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='group',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='title',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='meetingstomaterials',
            name='name',
            field=models.CharField(max_length=256),
        ),
    ]
