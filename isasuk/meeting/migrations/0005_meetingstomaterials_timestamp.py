# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('meeting', '0004_meeting_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='meetingstomaterials',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 28, 22, 20, 48, 679899), auto_now_add=True),
            preserve_default=False,
        ),
    ]
