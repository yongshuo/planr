# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Moneyer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('money_category', models.SmallIntegerField(blank=True, null=True, verbose_name=b'Money Category', choices=[(1, 'Income'), (2, 'Food'), (3, 'Traffic'), (4, 'Movie'), (-1, 'Other')])),
                ('credit', models.DecimalField(null=True, verbose_name=b'Credit', max_digits=10, decimal_places=2, blank=True)),
                ('debit', models.DecimalField(null=True, verbose_name=b'Debit', max_digits=10, decimal_places=2, blank=True)),
                ('remarks', models.TextField(null=True, verbose_name=b'Remarks', blank=True)),
                ('owner', models.ForeignKey(blank=True, to='users.EntityLogin', null=True)),
            ],
            options={
                'db_table': 'moneyer_manager',
            },
        ),
    ]
