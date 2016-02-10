# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meeting', '0004_auto_20160207_1519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
