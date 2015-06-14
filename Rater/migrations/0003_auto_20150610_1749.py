# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Rater', '0002_auto_20150609_1947'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rating',
            name='stars',
        ),
        migrations.AddField(
            model_name='rater',
            name='zip_code',
            field=models.CharField(default='00000', max_length=10),
        ),
        migrations.AddField(
            model_name='rating',
            name='rating',
            field=models.IntegerField(default=1, choices=[(1, '*'), (2, '**'), (3, '***'), (4, '****'), (5, '*****')]),
        ),
        migrations.AlterField(
            model_name='rater',
            name='gender',
            field=models.CharField(default='M', choices=[('M', 'Male'), ('F', 'Female')], max_length=1),
        ),
    ]
