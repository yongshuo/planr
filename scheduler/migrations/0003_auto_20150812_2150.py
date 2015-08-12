# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('scheduler', '0002_auto_20150808_1716'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='owner',
        ),
        migrations.AddField(
            model_name='event',
            name='owner',
            field=models.ForeignKey(blank=True, to='users.EntityLogin', null=True),
        ),
    ]
