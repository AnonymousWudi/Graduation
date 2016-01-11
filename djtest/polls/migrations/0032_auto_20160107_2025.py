# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0031_auto_20160107_2012'),
    ]

    operations = [
        migrations.RenameField(
            model_name='homework',
            old_name='hw_course',
            new_name='homework_course',
        ),
        migrations.RenameField(
            model_name='homework',
            old_name='hw_file',
            new_name='homework_file',
        ),
        migrations.RenameField(
            model_name='homework',
            old_name='hw_teacher',
            new_name='homework_teacher',
        ),
        migrations.RenameField(
            model_name='studenttohomework',
            old_name='sTh_file',
            new_name='sth_file',
        ),
        migrations.RenameField(
            model_name='studenttohomework',
            old_name='sTh_homework',
            new_name='sth_homework',
        ),
        migrations.RenameField(
            model_name='studenttohomework',
            old_name='sTh_student',
            new_name='sth_student',
        ),
        migrations.AlterField(
            model_name='user',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 7, 20, 24, 53, 790000), verbose_name=b'date upload'),
        ),
        migrations.AlterUniqueTogether(
            name='homework',
            unique_together=set([]),
        ),
        migrations.AlterUniqueTogether(
            name='studenttohomework',
            unique_together=set([]),
        ),
    ]
