# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0036_auto_20160108_1052'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursegroup',
            name='cg_repycg',
            field=models.CharField(default=b'', max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 11, 10, 33, 28, 229000), verbose_name=b'date upload'),
        ),
    ]
