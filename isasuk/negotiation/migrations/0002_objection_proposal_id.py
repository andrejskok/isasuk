# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('negotiation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='objection',
            name='proposal_id',
            field=models.CharField(null=True, blank=True, max_length=50),
        ),
    ]
