# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0016_auto_20151224_1815'),
    ]

    operations = [
        migrations.AddField(
            model_name='information',
            name='i_group',
            field=models.ForeignKey(default=None, to='polls.Group', null=True),
        ),
    ]
