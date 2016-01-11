# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_manager'),
    ]

    operations = [
        migrations.CreateModel(
            name='Academy',
            fields=[
                ('a_id', models.IntegerField(unique=True, serialize=False, primary_key=True)),
                ('a_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('c_id', models.CharField(max_length=20, unique=True, serialize=False, primary_key=True)),
                ('c_name', models.CharField(unique=True, max_length=40)),
                ('c_academy', models.ForeignKey(related_name='course_academy', to='polls.Academy')),
            ],
        ),
        migrations.CreateModel(
            name='Major',
            fields=[
                ('m_id', models.IntegerField(unique=True, serialize=False, primary_key=True)),
                ('m_name', models.CharField(max_length=30)),
                ('m_academy', models.ForeignKey(related_name='major_academy', to='polls.Academy')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('s_id', models.CharField(max_length=10, unique=True, serialize=False, primary_key=True)),
                ('s_name', models.CharField(max_length=10)),
                ('s_pwd', models.CharField(max_length=20)),
                ('s_mail', models.CharField(max_length=30)),
                ('s_class', models.IntegerField()),
                ('s_grade', models.IntegerField()),
                ('s_academy', models.ForeignKey(related_name='student_academy', to='polls.Academy')),
                ('s_major', models.ForeignKey(related_name='student_major', to='polls.Major')),
            ],
        ),
        migrations.CreateModel(
            name='StudentToCourse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('c_id', models.ForeignKey(related_name='get_course', to='polls.Course')),
                ('s_id', models.ForeignKey(related_name='get_student', to='polls.Student')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('t_id', models.CharField(max_length=20, unique=True, serialize=False, primary_key=True)),
                ('t_name', models.CharField(max_length=20)),
                ('t_pwd', models.CharField(max_length=20)),
                ('t_mail', models.CharField(max_length=20)),
                ('t_academy', models.ForeignKey(related_name='teacher_academy', to='polls.Academy')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='c_teacher',
            field=models.ForeignKey(related_name='course_teacher', to='polls.Teacher'),
        ),
        migrations.AlterUniqueTogether(
            name='studenttocourse',
            unique_together=set([('c_id', 's_id')]),
        ),
    ]
