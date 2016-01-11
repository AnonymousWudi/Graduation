# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0024_auto_20160105_1612'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ch_time', models.DateTimeField(verbose_name=b'date chat')),
                ('ch_person', models.CharField(max_length=30)),
                ('ch_message', models.TextField(max_length=140)),
                ('ch_type', models.CharField(max_length=10)),
                ('ch_course', models.ForeignKey(related_name='chat_course', to='polls.Course')),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 5, 17, 1, 28, 383000), verbose_name=b'date upload'),
        ),
    ]
