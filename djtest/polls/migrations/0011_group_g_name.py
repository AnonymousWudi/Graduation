# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0010_auto_20151223_1033'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='g_name',
            field=models.CharField(default=b'', max_length=30),
        ),
    ]
