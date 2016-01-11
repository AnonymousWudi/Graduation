# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0012_courseinformation_ci_total'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='courseinformation',
            name='ci_total',
        ),
    ]
