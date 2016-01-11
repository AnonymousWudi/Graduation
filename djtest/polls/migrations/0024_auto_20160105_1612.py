# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0023_auto_20160105_1558'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 5, 16, 12, 27, 560000), verbose_name=b'date upload'),
        ),
        migrations.AddField(
            model_name='user',
            name='uploadperson',
            field=models.ForeignKey(related_name='file_upperson', blank=True, to='polls.Teacher', null=True),
        ),
    ]
