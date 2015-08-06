# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_rating'),
        ('map', '0003_auto_20150711_1448'),
    ]

    operations = [
        migrations.AddField(
            model_name='point',
            name='rating',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='point',
            name='ratings',
            field=models.ManyToManyField(related_name='point_ratings', to='account.Rating'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='track',
            name='rating',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='track',
            name='ratings',
            field=models.ManyToManyField(related_name='track_ratings', to='account.Rating'),
            preserve_default=True,
        ),
    ]
