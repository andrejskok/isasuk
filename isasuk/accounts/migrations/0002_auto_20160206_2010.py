# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserDetails',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
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
            model_name='member',
            name='user',
        ),
        migrations.DeleteModel(
            name='Member',
        ),
    ]
