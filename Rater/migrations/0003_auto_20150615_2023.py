# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Rater', '0002_auto_20150615_2021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rater',
            name='zip_code',
            field=models.CharField(max_length=10),
        ),
    ]
