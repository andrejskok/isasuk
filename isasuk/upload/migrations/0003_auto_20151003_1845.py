# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0002_auto_20150928_2052'),
    ]

    operations = [
        migrations.CreateModel(
            name='Proposal',
            fields=[
                ('id', models.UUIDField(editable=False, serialize=False, default=uuid.uuid4, primary_key=True)),
                ('creator', models.CharField(max_length=50)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('state', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=80)),
            ],
        ),
        migrations.DeleteModel(
            name='Attachment',
        ),
        migrations.RemoveField(
            model_name='file',
            name='creator',
        ),
        migrations.RemoveField(
            model_name='file',
            name='state',
        ),
        migrations.AddField(
            model_name='file',
            name='file_type',
            field=models.CharField(default='attachment', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='file',
            name='proposal_id',
            field=models.CharField(default=12345, max_length=50),
            preserve_default=False,
        ),
    ]
