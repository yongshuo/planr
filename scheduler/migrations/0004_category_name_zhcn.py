# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0003_auto_20150812_2150'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='name_zhcn',
            field=models.TextField(null=True, verbose_name=b'Category Name (ZHCN)', blank=True),
        ),
    ]
