# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('negotiation', '0003_objection'),
    ]

    operations = [
        migrations.RenameField(
            model_name='objection',
            old_name='priority',
            new_name='importance',
        ),
    ]
