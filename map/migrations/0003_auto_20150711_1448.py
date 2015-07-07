# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0002_track_full_coordinates'),
    ]

    operations = [
        migrations.AddField(
            model_name='point',
            name='address_be',
            field=models.CharField(max_length=256, null=True, verbose_name='\u0410\u0434\u0440\u0435\u0441'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='point',
            name='address_en',
            field=models.CharField(max_length=256, null=True, verbose_name='\u0410\u0434\u0440\u0435\u0441'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='point',
            name='address_ru',
            field=models.CharField(max_length=256, null=True, verbose_name='\u0410\u0434\u0440\u0435\u0441'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='point',
            name='description_be',
            field=models.CharField(default=b'', max_length=256, null=True, verbose_name='\u041a\u0440\u0430\u0442\u043a\u043e\u0435 \u043e\u043f\u0438\u0441\u0430\u043d\u0438\u0435', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='point',
            name='description_en',
            field=models.CharField(default=b'', max_length=256, null=True, verbose_name='\u041a\u0440\u0430\u0442\u043a\u043e\u0435 \u043e\u043f\u0438\u0441\u0430\u043d\u0438\u0435', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='point',
            name='description_ru',
            field=models.CharField(default=b'', max_length=256, null=True, verbose_name='\u041a\u0440\u0430\u0442\u043a\u043e\u0435 \u043e\u043f\u0438\u0441\u0430\u043d\u0438\u0435', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='point',
            name='name_be',
            field=models.CharField(max_length=128, null=True, verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='point',
            name='name_en',
            field=models.CharField(max_length=128, null=True, verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='point',
            name='name_ru',
            field=models.CharField(max_length=128, null=True, verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='track',
            name='description_be',
            field=models.CharField(max_length=256, null=True, verbose_name='\u041a\u0440\u0430\u0442\u043a\u043e\u0435 \u043e\u043f\u0438\u0441\u0430\u043d\u0438\u0435'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='track',
            name='description_en',
            field=models.CharField(max_length=256, null=True, verbose_name='\u041a\u0440\u0430\u0442\u043a\u043e\u0435 \u043e\u043f\u0438\u0441\u0430\u043d\u0438\u0435'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='track',
            name='description_ru',
            field=models.CharField(max_length=256, null=True, verbose_name='\u041a\u0440\u0430\u0442\u043a\u043e\u0435 \u043e\u043f\u0438\u0441\u0430\u043d\u0438\u0435'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='track',
            name='name_be',
            field=models.CharField(max_length=128, null=True, verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='track',
            name='name_en',
            field=models.CharField(max_length=128, null=True, verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='track',
            name='name_ru',
            field=models.CharField(max_length=128, null=True, verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='location',
            name='admins',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name=b'locations'),
            preserve_default=True,
        ),
    ]
