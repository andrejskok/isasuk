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
            name='AdhocGroup',
            fields=[
                ('id', models.UUIDField(editable=False, primary_key=True, serialize=False, default=uuid.uuid4)),
                ('group_name', models.CharField(max_length=50)),
                ('member', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.UUIDField(editable=False, primary_key=True, serialize=False, default=uuid.uuid4)),
                ('group_name', models.CharField(max_length=50)),
                ('info', models.CharField(max_length=50, blank=True)),
                ('member', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
