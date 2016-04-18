# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_remove_group_end'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='end',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 17, 11, 21, 40, 169628, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
