# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Assignement',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, serialize=False, primary_key=True)),
                ('proposal_id', models.CharField(max_length=50)),
                ('group_name', models.CharField(max_length=50)),
                ('main_group', models.CharField(max_length=50)),
            ],
        ),
    ]
