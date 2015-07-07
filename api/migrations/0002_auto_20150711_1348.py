# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
        ('map', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='photos',
            field=models.ManyToManyField(to='map.Photo'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='message',
            name='point',
            field=models.ForeignKey(to='map.Point', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='message',
            name='track',
            field=models.ForeignKey(to='map.Track', null=True),
            preserve_default=True,
        ),
    ]
