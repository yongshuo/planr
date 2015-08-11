# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EntityLogin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('full_name', models.CharField(max_length=128, null=True, verbose_name=b'full name', blank=True)),
                ('search_text', models.CharField(max_length=1024, null=True, verbose_name=b'search text', blank=True)),
                ('email', models.CharField(max_length=128, null=True, verbose_name=b'email', blank=True)),
                ('password_hash', models.CharField(max_length=128, null=True, verbose_name=b'Hashed password', blank=True)),
                ('status', models.SmallIntegerField(default=1, null=True, verbose_name=b'status', blank=True, choices=[(1, 'Active'), (-1, 'Inactive'), (-2, 'Deleted')])),
                ('activation_code', models.CharField(help_text=b'Used for activating account by the activation link', max_length=128, null=True, verbose_name=b'Activation Code', blank=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name=b'create time')),
            ],
            options={
                'db_table': 'users_entitylogin',
            },
        ),
    ]
