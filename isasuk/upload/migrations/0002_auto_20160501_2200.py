# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file_type',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='file',
            name='name',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='file',
            name='path',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='file',
            name='proposal_id',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='category',
            field=models.CharField(max_length=256, blank=True),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='name',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='state',
            field=models.CharField(max_length=256),
        ),
    ]
