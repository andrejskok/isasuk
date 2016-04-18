# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('meeting', '0005_meetingstomaterials_timestamp'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AdhocGroup',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, serialize=False, primary_key=True)),
                ('group_name', models.CharField(max_length=50)),
                ('member', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, serialize=False, primary_key=True)),
                ('state', models.CharField(max_length=50, blank=True)),
                ('meeting', models.ForeignKey(to='meeting.Meeting')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, serialize=False, primary_key=True)),
                ('group_name', models.CharField(max_length=50)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('is_chair', models.BooleanField()),
                ('member', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
