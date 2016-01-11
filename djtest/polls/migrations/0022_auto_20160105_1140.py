# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0021_auto_20160105_1119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='headImg',
            field=models.FileField(upload_to=b'upload/%Y%m%d'),
        ),
    ]
