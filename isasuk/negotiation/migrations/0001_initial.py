# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Archive',
            fields=[
                ('id', models.UUIDField(primary_key=True, editable=False, serialize=False, default=uuid.uuid4)),
                ('proposal_id', models.CharField(max_length=50)),
                ('path', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('file_type', models.CharField(max_length=50)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Assignement',
            fields=[
                ('id', models.UUIDField(primary_key=True, editable=False, serialize=False, default=uuid.uuid4)),
                ('proposal_id', models.CharField(max_length=50)),
                ('group_name', models.CharField(max_length=50)),
                ('main_group', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Objection',
            fields=[
                ('id', models.UUIDField(primary_key=True, editable=False, serialize=False, default=uuid.uuid4)),
                ('file_id', models.CharField(max_length=50)),
                ('original_text', models.CharField(max_length=5000)),
                ('objection', models.CharField(max_length=5000)),
                ('importance', models.CharField(max_length=50)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user_id', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.UUIDField(primary_key=True, editable=False, serialize=False, default=uuid.uuid4)),
                ('proposal_id', models.CharField(max_length=50)),
                ('reason', models.CharField(max_length=1500)),
            ],
        ),
    ]
