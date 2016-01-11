# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0015_auto_20151224_1620'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='information',
            name='id',
        ),
        migrations.AddField(
            model_name='information',
            name='i_id',
            field=models.AutoField(default=1, serialize=False, primary_key=True),
        ),
    ]
