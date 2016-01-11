# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0008_courseinformation_ci_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('g_course', models.ForeignKey(related_name='group_course', to='polls.Course')),
                ('g_teacher', models.ForeignKey(related_name='group_teacher', to='polls.Teacher')),
            ],
        ),
        migrations.CreateModel(
            name='StudentToGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('g_id', models.ForeignKey(related_name='sTg_group', to='polls.Group')),
                ('s_id', models.ForeignKey(related_name='sTg_student', to='polls.Student')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='studenttogroup',
            unique_together=set([('s_id', 'g_id')]),
        ),
        migrations.AlterUniqueTogether(
            name='group',
            unique_together=set([('g_teacher', 'g_course')]),
        ),
    ]
