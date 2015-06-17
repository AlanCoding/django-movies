# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Rater', '0005_auto_20150617_2019'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='total_save',
            field=models.IntegerField(null=True),
        ),
    ]
