# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.TextField(null=True, verbose_name=b'Project Title', blank=True)),
                ('description', models.TextField(null=True, verbose_name=b'Description', blank=True)),
                ('color', models.CharField(max_length=64, null=True, verbose_name=b'Color', blank=True)),
                ('owner', models.ForeignKey(blank=True, to='users.EntityLogin', null=True)),
            ],
            options={
                'db_table': 'gantter_project',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.TextField(null=True, verbose_name=b'Title', blank=True)),
                ('task_id', models.SmallIntegerField(null=True, verbose_name=b'Task ID', blank=True)),
                ('order_id', models.SmallIntegerField(null=True, verbose_name=b'Order ID', blank=True)),
                ('start', models.DateField(null=True, verbose_name=b'Start Date', blank=True)),
                ('end', models.DateField(null=True, verbose_name=b'End Date', blank=True)),
                ('percentage_complete', models.DecimalField(null=True, verbose_name=b'Percentage Completed', max_digits=b'5', decimal_places=b'2', blank=True)),
                ('summary', models.BooleanField(default=True, verbose_name=b'Summary ?')),
                ('expand', models.BooleanField(default=True, verbose_name=b'Expand ?')),
                ('parent', models.ForeignKey(blank=True, to='gantter.Task', null=True)),
                ('project', models.ForeignKey(blank=True, to='gantter.Project', null=True)),
            ],
            options={
                'db_table': 'gantter_task',
            },
        ),
        migrations.CreateModel(
            name='TaskDependency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dtype', models.SmallIntegerField(null=True, verbose_name=b'Type', blank=True)),
                ('predecessor', models.ForeignKey(related_name='predecessor', blank=True, to='gantter.Task', null=True)),
                ('successor', models.ForeignKey(related_name='successor', blank=True, to='gantter.Task', null=True)),
            ],
            options={
                'db_table': 'gantter_task_dependency',
            },
        ),
    ]
