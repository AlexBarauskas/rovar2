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
            name='gender',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='\u041f\u043e\u043b', choices=[('male', '\u041c\u0443\u0436\u0441\u043a\u043e\u0439'), ('female', '\u0416\u0435\u043d\u0441\u043a\u0438\u0439')]),
            preserve_default=True,
        ),
    ]
