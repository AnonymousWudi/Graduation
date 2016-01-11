# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0013_remove_courseinformation_ci_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='c_number',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='course',
            name='c_total',
            field=models.IntegerField(default=100),
        ),
    ]
