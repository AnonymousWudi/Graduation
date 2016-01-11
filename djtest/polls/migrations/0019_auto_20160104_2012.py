# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0018_auto_20151225_1455'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('n_id', models.AutoField(serialize=False, primary_key=True)),
                ('n_type', models.IntegerField(default=0)),
                ('n_from', models.CharField(default=b'0', max_length=30)),
                ('n_to', models.CharField(default=b'0', max_length=30)),
                ('n_title', models.CharField(default=b'system', max_length=30)),
                ('n_message', models.TextField(blank=True)),
                ('n_time', models.DateTimeField(verbose_name=b'data send')),
                ('n_status', models.BooleanField(default=False)),
                ('n_course', models.ForeignKey(default=None, blank=True, to='polls.Course', null=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='notice',
            unique_together=set([('n_id', 'n_time')]),
        ),
    ]
