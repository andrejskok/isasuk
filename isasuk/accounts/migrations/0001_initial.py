# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Details',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('faculty', models.CharField(blank=True, max_length=100, null=True)),
                ('title_before', models.CharField(blank=True, max_length=100, null=True)),
                ('title_after', models.CharField(blank=True, max_length=100, null=True)),
                ('role', models.CharField(max_length=100)),
                ('start', models.CharField(max_length=100)),
                ('end', models.CharField(max_length=100)),
                ('is_student', models.BooleanField()),
                ('is_member', models.BooleanField()),
                ('is_chair', models.BooleanField()),
                ('can_submit', models.BooleanField()),
                ('is_active', models.BooleanField()),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
