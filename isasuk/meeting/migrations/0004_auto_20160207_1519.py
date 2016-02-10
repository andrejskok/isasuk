# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meeting', '0003_auto_20151004_2017'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='group',
            field=models.CharField(default=False, max_length=80),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='meeting',
            name='invitation',
            field=models.CharField(default='ahoj', max_length=80),
            preserve_default=False,
        ),
    ]
