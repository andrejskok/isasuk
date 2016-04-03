# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('negotiation', '0003_remove_objection_proposal_id'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Archive',
            new_name='History',
        ),
        migrations.RenameField(
            model_name='history',
            old_name='proposal_id',
            new_name='meeting_id',
        ),
    ]
