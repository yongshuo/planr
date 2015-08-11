# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='end_time_zone',
            field=models.CharField(max_length=128, null=True, verbose_name=b'End Timezone', blank=True),
        ),
        migrations.AddField(
            model_name='event',
            name='start_time_zone',
            field=models.CharField(max_length=128, null=True, verbose_name=b'Start Timezone', blank=True),
        ),
    ]
