# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0030_auto_20160107_1529'),
    ]

    operations = [
        migrations.CreateModel(
            name='Homework',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hw_title', models.CharField(default=b'\xe4\xbd\x9c\xe4\xb8\x9a', max_length=30)),
                ('hw_message', models.TextField(default=None, null=True, blank=True)),
                ('hw_starttime', models.DateTimeField()),
                ('hw_deadline', models.DateTimeField()),
                ('hw_score', models.IntegerField(default=100)),
                ('hw_course', models.ForeignKey(to='polls.Course')),
            ],
        ),
        migrations.CreateModel(
            name='StudentToHomework',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sTh_time', models.DateTimeField()),
                ('sTh_status', models.IntegerField(default=1)),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='headImg',
            field=models.FileField(upload_to=b'./polls/media/upload/'),
        ),
        migrations.AlterField(
            model_name='user',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 7, 20, 12, 47, 778000), verbose_name=b'date upload'),
        ),
        migrations.AddField(
            model_name='studenttohomework',
            name='sTh_file',
            field=models.ForeignKey(to='polls.User'),
        ),
        migrations.AddField(
            model_name='studenttohomework',
            name='sTh_homework',
            field=models.ForeignKey(to='polls.Homework'),
        ),
        migrations.AddField(
            model_name='studenttohomework',
            name='sTh_student',
            field=models.ForeignKey(to='polls.Student'),
        ),
        migrations.AddField(
            model_name='homework',
            name='hw_file',
            field=models.ForeignKey(blank=True, to='polls.User', null=True),
        ),
        migrations.AddField(
            model_name='homework',
            name='hw_teacher',
            field=models.ForeignKey(to='polls.Teacher'),
        ),
        migrations.AlterUniqueTogether(
            name='studenttohomework',
            unique_together=set([('sTh_homework', 'sTh_time')]),
        ),
        migrations.AlterUniqueTogether(
            name='homework',
            unique_together=set([('hw_title', 'hw_course')]),
        ),
    ]
