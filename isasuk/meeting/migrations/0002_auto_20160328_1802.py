# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meeting', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meeting',
            name='conclusion',
        ),
        migrations.RemoveField(
            model_name='meeting',
            name='invitation',
        ),
        migrations.RemoveField(
            model_name='meeting',
            name='program',
        ),
    ]
