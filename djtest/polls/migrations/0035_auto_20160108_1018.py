# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0034_auto_20160107_2126'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homework',
            name='homework_course',
        ),
        migrations.RemoveField(
            model_name='homework',
            name='homework_file',
        ),
        migrations.RemoveField(
            model_name='homework',
            name='homework_teacher',
        ),
        migrations.RemoveField(
            model_name='studenttohomework',
            name='sth_file',
        ),
        migrations.RemoveField(
            model_name='studenttohomework',
            name='sth_homework',
        ),
        migrations.RemoveField(
            model_name='studenttohomework',
            name='sth_student',
        ),
        migrations.AddField(
            model_name='homework',
            name='hw_course',
            field=models.ForeignKey(related_name='homework_course', default=None, blank=True, to='polls.Course', null=True),
        ),
        migrations.AddField(
            model_name='homework',
            name='hw_file',
            field=models.ForeignKey(related_name='homework_file', blank=True, to='polls.User', null=True),
        ),
        migrations.AddField(
            model_name='homework',
            name='hw_teacher',
            field=models.ForeignKey(related_name='homework_teacher', blank=True, to='polls.Teacher', null=True),
        ),
        migrations.AddField(
            model_name='studenttohomework',
            name='sTh_file',
            field=models.ForeignKey(related_name='sth_file', blank=True, to='polls.User', null=True),
        ),
        migrations.AddField(
            model_name='studenttohomework',
            name='sTh_homework',
            field=models.ForeignKey(related_name='sth_homework', blank=True, to='polls.Homework', null=True),
        ),
        migrations.AddField(
            model_name='studenttohomework',
            name='sTh_student',
            field=models.ForeignKey(related_name='sth_student', blank=True, to='polls.Student', null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 8, 10, 18, 3, 880000), verbose_name=b'date upload'),
        ),
    ]
