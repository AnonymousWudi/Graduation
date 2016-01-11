# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0025_auto_20160105_1701'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cg_type', models.IntegerField(default=0)),
                ('cg_author', models.CharField(default=b'0', max_length=10)),
                ('cg_title', models.CharField(default=b'\xe8\xae\xa8\xe8\xae\xba\xe5\x8c\xba', max_length=50)),
                ('cg_time', models.DateTimeField(verbose_name=b'group_datetime')),
                ('cg_replynumber', models.IntegerField(default=0, null=True)),
                ('cg_course', models.ForeignKey(to='polls.Course')),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 6, 20, 42, 38, 929000), verbose_name=b'date upload'),
        ),
    ]
