# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0017_information_i_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='information',
            name='i_group',
            field=models.ForeignKey(default=None, blank=True, to='polls.Group', null=True),
        ),
        migrations.AlterField(
            model_name='information',
            name='i_id',
            field=models.AutoField(serialize=False, primary_key=True),
        ),
    ]
