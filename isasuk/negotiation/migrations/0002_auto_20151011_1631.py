# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('negotiation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignement',
            name='main_group',
            field=models.BooleanField(default=False),
        ),
    ]
