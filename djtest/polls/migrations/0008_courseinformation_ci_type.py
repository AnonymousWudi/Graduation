# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0007_auto_20151222_1209'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseinformation',
            name='ci_type',
            field=models.IntegerField(default=0),
        ),
    ]
