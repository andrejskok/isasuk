# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meeting', '0005_meetingstomaterials_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meetingstomaterials',
            name='proposal',
            field=models.ForeignKey(to='upload.Proposal', null=True, blank=True),
        ),
    ]
