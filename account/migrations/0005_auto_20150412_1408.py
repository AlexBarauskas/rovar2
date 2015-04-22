# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20150410_1938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='address',
            field=models.CharField(max_length=255, verbose_name='\u0410\u0434\u0440\u0435\u0441', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='bike',
            field=models.CharField(max_length=255, verbose_name='\u0411\u0430\u0439\u043a', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=255, null=True, verbose_name='\u0415\u043c\u0430\u0439\u043b', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=255, verbose_name='\u0418\u043c\u044f', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(max_length=10, null=True, verbose_name='\u041f\u043e\u043b', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='\u0410\u043a\u0442\u0438\u0432\u0435\u043d?'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='is_admin',
            field=models.BooleanField(default=False, verbose_name='\u0410\u0434\u043c\u0438\u043d\u0438\u0441\u0442\u0440\u0430\u0442\u043e\u0440?'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=255, verbose_name='\u0424\u0430\u043c\u0438\u043b\u0438\u044f', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=255, unique=True, null=True, verbose_name='\u0422\u0435\u043b\u0435\u0444\u043e\u043d', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(unique=True, max_length=255, verbose_name='\u041f\u0441\u0435\u0432\u0434\u043e\u043d\u0438\u043c'),
            preserve_default=True,
        ),
    ]
