# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_rating'),
        ('blog', '0002_auto_20150702_0043'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='rating',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='ratings',
            field=models.ManyToManyField(related_name='post_ratings', to='account.Rating'),
            preserve_default=True,
        ),
    ]
