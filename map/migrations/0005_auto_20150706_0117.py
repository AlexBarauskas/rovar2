# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0004_auto_20150619_2043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='admins',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name=b'locations'),
            preserve_default=True,
        ),
    ]
