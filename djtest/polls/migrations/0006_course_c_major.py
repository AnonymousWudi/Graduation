# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_remove_course_c_major'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='c_major',
            field=models.ForeignKey(related_name='course_major', default=None, to='polls.Major'),
        ),
    ]
