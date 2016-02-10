# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.UUIDField(editable=False, primary_key=True, default=uuid.uuid4, serialize=False)),
                ('file_id', models.CharField(max_length=50)),
                ('path', models.CharField(max_length=50)),
                ('creator', models.CharField(max_length=50)),
                ('timestamp', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.UUIDField(editable=False, primary_key=True, default=uuid.uuid4, serialize=False)),
                ('path', models.CharField(max_length=50)),
                ('creator', models.CharField(max_length=50)),
                ('timestamp', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=50)),
            ],
        ),
    ]
