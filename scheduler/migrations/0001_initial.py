# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField(null=True, verbose_name=b'Category Name', blank=True)),
                ('color', models.CharField(max_length=64, null=True, verbose_name=b'Category color', blank=True)),
                ('owner', models.ForeignKey(blank=True, to='users.EntityLogin', null=True)),
            ],
            options={
                'db_table': 'scheduler_category',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.TextField(null=True, verbose_name=b'Title', blank=True)),
                ('start_date', models.DateField(help_text=b'Blank if not all day event', null=True, verbose_name=b'Start Date', blank=True)),
                ('start_date_time', models.DateTimeField(null=True, verbose_name=b'Start Time', blank=True)),
                ('to_date', models.DateField(null=True, verbose_name=b'To Date', blank=True)),
                ('to_date_time', models.DateTimeField(null=True, verbose_name=b'To Time', blank=True)),
                ('recurrenceID', models.CharField(max_length=128, null=True, verbose_name=b'Recurrence ID', blank=True)),
                ('recurrenceRule', models.TextField(null=True, verbose_name=b'Recurrence Rule', blank=True)),
                ('recurrenceException', models.TextField(null=True, verbose_name=b'Recurrence Exception', blank=True)),
                ('isAllDay', models.BooleanField(default=False, verbose_name=b'Is all day')),
                ('description', models.TextField(null=True, verbose_name=b'Description', blank=True)),
                ('category', models.ForeignKey(blank=True, to='scheduler.Category', null=True)),
            ],
            options={
                'db_table': 'scheduler_event',
            },
        ),
    ]
