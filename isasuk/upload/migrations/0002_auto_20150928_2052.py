# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='attachment',
            name='name',
            field=models.CharField(max_length=50, default='aaa'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='file',
            name='name',
            field=models.CharField(max_length=50, default='aaa'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='attachment',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='file',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
