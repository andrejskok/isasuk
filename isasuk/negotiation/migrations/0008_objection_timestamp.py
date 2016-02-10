# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('negotiation', '0007_archive'),
    ]

    operations = [
        migrations.AddField(
            model_name='objection',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 11, 3, 22, 51, 28, 120221, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
