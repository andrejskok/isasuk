# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_remove_details_end'),
    ]

    operations = [
        migrations.AddField(
            model_name='details',
            name='end',
            field=models.CharField(max_length=100, default=datetime.datetime(2016, 4, 17, 13, 26, 46, 169527, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
