# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20160206_2043'),
    ]

    operations = [
        migrations.AddField(
            model_name='details',
            name='can_submit',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
