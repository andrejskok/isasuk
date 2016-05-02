# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('negotiation', '0004_auto_20160403_1953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignement',
            name='group_name',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='assignement',
            name='proposal_id',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='history',
            name='file_type',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='history',
            name='meeting_id',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='history',
            name='name',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='history',
            name='path',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='objection',
            name='file_id',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='objection',
            name='importance',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='report',
            name='proposal_id',
            field=models.CharField(max_length=256),
        ),
    ]
