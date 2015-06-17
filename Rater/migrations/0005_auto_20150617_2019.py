# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Rater', '0004_movie_avg_save'),
    ]

    operations = [
        migrations.AddField(
            model_name='genre',
            name='Nmovies_save',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='genre',
            name='Nratings_save',
            field=models.IntegerField(null=True),
        ),
    ]
