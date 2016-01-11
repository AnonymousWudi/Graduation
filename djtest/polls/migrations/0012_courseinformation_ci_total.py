# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0011_group_g_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseinformation',
            name='ci_total',
            field=models.IntegerField(default=100),
        ),
    ]
