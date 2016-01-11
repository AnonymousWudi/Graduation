# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_course_c_major'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='c_major',
        ),
    ]
