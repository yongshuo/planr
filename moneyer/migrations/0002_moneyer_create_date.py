# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moneyer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='moneyer',
            name='create_date',
            field=models.DateField(null=True, verbose_name=b'Create Date', blank=True),
        ),
    ]
