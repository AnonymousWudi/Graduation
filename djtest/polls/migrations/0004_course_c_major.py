# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_auto_20151221_1337'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='c_major',
            field=models.ForeignKey(related_name='course_major', to='polls.Major'),
            preserve_default=False,
        ),
    ]
