# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('negotiation', '0002_auto_20151011_1631'),
    ]

    operations = [
        migrations.CreateModel(
            name='Objection',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False, editable=False, default=uuid.uuid4)),
                ('proposal_id', models.CharField(max_length=50)),
                ('file_id', models.CharField(max_length=50)),
                ('original_text', models.CharField(max_length=5000)),
                ('objection', models.CharField(max_length=5000)),
                ('priority', models.CharField(max_length=50)),
            ],
        ),
    ]
