# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0001_initial'),
        ('meeting', '0002_auto_20160328_1802'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='conclusion',
            field=models.ForeignKey(to='upload.File', related_name='meeting_conclusion', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meeting',
            name='invitation',
            field=models.ForeignKey(to='upload.File', related_name='meeting_invitation', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meeting',
            name='program',
            field=models.ForeignKey(to='upload.File', related_name='meeting_program', null=True, blank=True),
        ),
    ]
