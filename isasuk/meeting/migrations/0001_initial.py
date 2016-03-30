# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('creator', models.CharField(max_length=80)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=80)),
                ('date', models.DateTimeField()),
                ('group', models.CharField(max_length=80)),
                ('closed', models.BooleanField(default=False)),
                ('conclusion', models.ForeignKey(related_name='meeting_conclusion', blank=True, null=True, to='upload.File')),
                ('invitation', models.ForeignKey(related_name='meeting_invitation', blank=True, null=True, to='upload.File')),
                ('program', models.ForeignKey(related_name='meeting_program', blank=True, null=True, to='upload.File')),
            ],
        ),
        migrations.CreateModel(
            name='MeetingsToMaterials',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=80)),
                ('order', models.IntegerField()),
                ('conclusion', models.ForeignKey(related_name='m2m_conclusion', blank=True, null=True, to='upload.File')),
                ('meeting', models.ForeignKey(to='meeting.Meeting')),
                ('proposal', models.ForeignKey(to='upload.Proposal')),
                ('title', models.ForeignKey(blank=True, null=True, to='upload.File')),
            ],
        ),
    ]
