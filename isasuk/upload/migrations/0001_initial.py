# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import uuid
import isasuk.upload.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.UUIDField(editable=False, serialize=False, primary_key=True, default=uuid.uuid4)),
                ('proposal_id', models.CharField(max_length=50)),
                ('path', models.CharField(max_length=50)),
                ('file', models.FileField(upload_to=isasuk.upload.models.generate_filename)),
                ('name', models.CharField(max_length=50)),
                ('file_type', models.CharField(max_length=50)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Proposal',
            fields=[
                ('id', models.UUIDField(editable=False, serialize=False, primary_key=True, default=uuid.uuid4)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('state', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=80)),
                ('category', models.CharField(max_length=50, blank=True)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
