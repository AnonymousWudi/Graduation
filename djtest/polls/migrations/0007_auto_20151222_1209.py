# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_course_c_major'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseInformation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ci_period', models.IntegerField()),
                ('ci_time', models.IntegerField()),
                ('ci_classroom', models.CharField(max_length=30)),
                ('ci_module', models.IntegerField()),
                ('ci_id', models.ForeignKey(related_name='course_info', to='polls.Course')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='courseinformation',
            unique_together=set([('ci_id', 'ci_time')]),
        ),
    ]
