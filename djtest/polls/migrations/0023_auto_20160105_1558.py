# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0022_auto_20160105_1140'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='course',
            field=models.ForeignKey(related_name='file_course', blank=True, to='polls.Course', null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='headImg',
            field=models.FileField(upload_to=b'/'),
        ),
    ]
