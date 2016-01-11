# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0009_auto_20151222_2132'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='g_number',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='group',
            name='g_total',
            field=models.IntegerField(default=0),
        ),
    ]
