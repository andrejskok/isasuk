# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('negotiation', '0004_auto_20151012_2157'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.UUIDField(editable=False, primary_key=True, serialize=False, default=uuid.uuid4)),
                ('proposal_id', models.CharField(max_length=50)),
                ('reason', models.CharField(max_length=1500)),
            ],
        ),
    ]
