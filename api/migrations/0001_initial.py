# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import api.models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uid', models.CharField(default=api.models.make_uid, unique=True, max_length=56)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('state', models.CharField(default=b'm', max_length=1, choices=[(b'm', '\u041d\u0430 \u0440\u0430\u0441\u0441\u043c\u043e\u0442\u0440\u0435\u043d\u0438\u0438 \u043c\u043e\u0434\u0435\u0440\u0430\u0442\u043e\u0440\u043e\u043c'), (b'f', '\u0414\u043b\u044f \u043e\u0442\u043f\u0440\u0430\u0432\u043a\u0438'), (b's', '\u041e\u0442\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u043e'), (b'r', '\u041f\u0440\u043e\u0447\u0438\u0442\u0430\u043d\u043e')])),
                ('method', models.CharField(default=b'a', max_length=1, choices=[(b'a', '\u0414\u043e\u0431\u0430\u0432\u043b\u0435\u043d\u0438\u0435 \u0442\u043e\u0447\u043a\u0438'), (b'u', '\u041f\u0440\u0435\u0434\u043b\u043e\u0436\u0435\u043d\u0438\u0435 \u043d\u0430 \u0438\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u0435')])),
                ('message', models.TextField(default='\u0412\u0430\u0448\u0435 \u043f\u0440\u0435\u0434\u043b\u043e\u0436\u0435\u043d\u0438\u0435 \u043f\u0440\u0438\u043d\u044f\u0442\u043e.')),
                ('email', models.EmailField(max_length=75, null=True)),
                ('description', models.TextField(default=b'', null=True, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435')),
                ('app', models.ForeignKey(to='api.Application')),
                ('photos', models.ManyToManyField(to='map.Photo')),
                ('point', models.ForeignKey(to='map.Point', null=True)),
                ('track', models.ForeignKey(to='map.Track', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
