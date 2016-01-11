# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0027_auto_20160106_2052'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursegroup',
            name='cg_message',
            field=models.TextField(default=b'', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 7, 14, 25, 34, 899000), verbose_name=b'date upload'),
        ),
    ]
