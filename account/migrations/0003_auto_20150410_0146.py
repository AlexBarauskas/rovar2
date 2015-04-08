# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20150410_0142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=255, null=True, verbose_name=b'\xd0\x95\xd0\xbc\xd0\xb0\xd0\xb9\xd0\xbb', blank=True),
            preserve_default=True,
        ),
    ]
