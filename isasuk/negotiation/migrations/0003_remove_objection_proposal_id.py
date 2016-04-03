# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('negotiation', '0002_objection_proposal_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='objection',
            name='proposal_id',
        ),
    ]
