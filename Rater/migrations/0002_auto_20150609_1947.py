# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Rater', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rater',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('age', models.IntegerField(default=0)),
                ('gender', models.IntegerField(default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='rating',
            name='user',
        ),
        migrations.AddField(
            model_name='movie',
            name='release_date',
            field=models.IntegerField(default=1990),
        ),
        migrations.AddField(
            model_name='movie',
            name='title',
            field=models.CharField(max_length=200, default='unknown'),
        ),
        migrations.AddField(
            model_name='rating',
            name='movie',
            field=models.ForeignKey(to='Rater.Movie', default=1),
        ),
        migrations.AddField(
            model_name='rating',
            name='stars',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='rating',
            name='rater',
            field=models.ForeignKey(to='Rater.Rater', default=1),
        ),
    ]
