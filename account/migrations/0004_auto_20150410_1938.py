# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20150410_0146'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(max_length=10, null=True, verbose_name=b'\xd0\x9f\xd0\xbe\xd0\xbb', blank=True),
            preserve_default=True,
        ),
    ]
