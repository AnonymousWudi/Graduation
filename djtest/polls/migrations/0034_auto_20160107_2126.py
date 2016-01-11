# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0033_auto_20160107_2126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 7, 21, 26, 33, 182000), verbose_name=b'date upload'),
        ),
    ]
