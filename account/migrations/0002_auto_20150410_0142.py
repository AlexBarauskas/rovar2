# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=255, unique=True, null=True, verbose_name=b'\xd0\x95\xd0\xbc\xd0\xb0\xd0\xb9\xd0\xbb', blank=True),
            preserve_default=True,
        ),
    ]
