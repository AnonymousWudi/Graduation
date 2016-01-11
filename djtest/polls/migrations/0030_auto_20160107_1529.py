# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0029_auto_20160107_1425'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='type',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='coursegroup',
            name='cg_message',
            field=models.TextField(default=None, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 7, 15, 29, 2, 315000), verbose_name=b'date upload'),
        ),
        migrations.AlterField(
            model_name='user',
            name='uploadperson',
            field=models.CharField(default=b'0', max_length=20),
        ),
    ]
