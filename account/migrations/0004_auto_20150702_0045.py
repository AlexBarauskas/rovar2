# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20150702_0029'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='description_be',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='author',
            name='description_en',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='author',
            name='description_ru',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='author',
            name='name_be',
            field=models.CharField(max_length=128, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='author',
            name='name_en',
            field=models.CharField(max_length=128, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='author',
            name='name_ru',
            field=models.CharField(max_length=128, null=True),
            preserve_default=True,
        ),
    ]
