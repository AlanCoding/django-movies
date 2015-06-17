# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Rater', '0003_auto_20150615_2023'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='avg_save',
            field=models.FloatField(null=True),
        ),
    ]
