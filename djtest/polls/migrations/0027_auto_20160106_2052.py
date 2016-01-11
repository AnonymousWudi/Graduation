# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0026_auto_20160106_2042'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursegroup',
            name='cg_file',
            field=models.ForeignKey(default=None, blank=True, to='polls.User', null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 6, 20, 52, 15, 812000), verbose_name=b'date upload'),
        ),
    ]
