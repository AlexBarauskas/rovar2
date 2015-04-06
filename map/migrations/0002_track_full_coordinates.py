# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='track',
            name='full_coordinates',
            field=models.TextField(default=b'[]', verbose_name='\u041a\u043e\u043e\u0440\u0434\u0438\u043d\u0430\u0442\u044b'),
            preserve_default=True,
        ),
    ]
