# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0002_auto_20160206_2010'),
    ]

    operations = [
        migrations.CreateModel(
            name='Details',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('role', models.CharField(max_length=100)),
                ('start', models.CharField(max_length=100)),
                ('end', models.CharField(max_length=100)),
                ('is_admin', models.BooleanField()),
                ('is_student', models.BooleanField()),
                ('is_member', models.BooleanField()),
                ('is_chair', models.BooleanField()),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='userdetails',
            name='user',
        ),
        migrations.DeleteModel(
            name='UserDetails',
        ),
    ]
