# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
        ('map', '0002_track_full_coordinates'),
    ]

    operations = [
        migrations.AddField(
            model_name='point',
            name='post',
            field=models.OneToOneField(null=True, to='blog.Post'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='track',
            name='post',
            field=models.OneToOneField(null=True, to='blog.Post'),
            preserve_default=True,
        ),
    ]
