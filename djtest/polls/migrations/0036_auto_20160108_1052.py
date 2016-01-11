# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0035_auto_20160108_1018'),
    ]

    operations = [
        migrations.AddField(
            model_name='homework',
            name='hw_status',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='user',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 8, 10, 52, 32, 983000), verbose_name=b'date upload'),
        ),
    ]
