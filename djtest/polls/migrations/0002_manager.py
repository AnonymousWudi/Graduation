# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('m_name', models.CharField(max_length=20, unique=True, serialize=False, primary_key=True)),
                ('m_pwd', models.CharField(max_length=20)),
            ],
        ),
    ]
