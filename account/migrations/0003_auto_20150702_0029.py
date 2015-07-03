# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20150619_2043'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('username', models.CharField(unique=True, max_length=255, verbose_name=b'\xd0\x9f\xd1\x81\xd0\xb5\xd0\xb2\xd0\xb4\xd0\xbe\xd0\xbd\xd0\xb8\xd0\xbc')),
                ('email', models.EmailField(unique=True, max_length=255, verbose_name=b'\xd0\x95\xd0\xbc\xd0\xb0\xd0\xb9\xd0\xbb')),
                ('img_url', models.URLField(null=True)),
                ('phone', models.CharField(max_length=255, unique=True, null=True, verbose_name=b'\xd0\xa2\xd0\xb5\xd0\xbb\xd0\xb5\xd1\x84\xd0\xbe\xd0\xbd', blank=True)),
                ('bike', models.CharField(max_length=255, verbose_name=b'\xd0\x91\xd0\xb0\xd0\xb9\xd0\xba', blank=True)),
                ('backend', models.CharField(max_length=16, null=True, choices=[('vk', '\u0412\u041a\u043e\u043d\u0442\u0430\u043a\u0442\u0435'), ('twitter', 'Twitter'), ('facebook', 'Facebook')])),
                ('id_from_backend', models.CharField(max_length=32, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True, verbose_name=b'\xd0\x90\xd0\xba\xd1\x82\xd0\xb8\xd0\xb2\xd0\xb5\xd0\xbd?')),
                ('is_admin', models.BooleanField(default=False, verbose_name=b'\xd0\x90\xd0\xb4\xd0\xbc\xd0\xb8\xd0\xbd\xd0\xb8\xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80?')),
            ],
            options={
                'verbose_name': '\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c',
                'verbose_name_plural': '\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0438',
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='account',
            name='user',
        ),
        migrations.DeleteModel(
            name='Account',
        ),
    ]
