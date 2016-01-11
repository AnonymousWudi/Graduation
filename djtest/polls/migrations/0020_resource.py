# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0019_auto_20160104_2012'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('r_filename', models.CharField(max_length=30)),
                ('r_file', models.FileField(upload_to=b'upload/%Y%m%d')),
            ],
        ),
    ]
