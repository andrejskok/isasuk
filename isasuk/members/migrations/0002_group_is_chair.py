# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='is_chair',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
