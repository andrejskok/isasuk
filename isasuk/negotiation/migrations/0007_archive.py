# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('negotiation', '0006_objection_user_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Archive',
            fields=[
                ('id', models.UUIDField(serialize=False, default=uuid.uuid4, editable=False, primary_key=True)),
                ('proposal_id', models.CharField(max_length=50)),
                ('path', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('file_type', models.CharField(max_length=50)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
