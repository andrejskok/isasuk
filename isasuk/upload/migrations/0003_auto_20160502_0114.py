# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import isasuk.upload.models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0002_auto_20160501_2200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(upload_to=isasuk.upload.models.generate_filename, max_length=1000),
        ),
    ]
