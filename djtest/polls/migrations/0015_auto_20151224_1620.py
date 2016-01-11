# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0014_auto_20151224_1449'),
    ]

    operations = [
        migrations.CreateModel(
            name='Information',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('i_type', models.IntegerField(default=2)),
                ('i_from', models.CharField(default=b'0', max_length=30)),
                ('i_to', models.CharField(default=b'0', max_length=30)),
                ('i_title', models.CharField(default=b'system', max_length=30)),
                ('i_message', models.TextField(blank=True)),
                ('i_time', models.DateTimeField(verbose_name=b'date send')),
                ('i_status', models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='information',
            unique_together=set([('i_from', 'i_to', 'i_time')]),
        ),
    ]
