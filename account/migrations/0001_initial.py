# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('first_name', models.CharField(max_length=255, verbose_name='\u0418\u043c\u044f', blank=True)),
                ('last_name', models.CharField(max_length=255, verbose_name='\u0424\u0430\u043c\u0438\u043b\u0438\u044f', blank=True)),
                ('username', models.CharField(unique=True, max_length=255, verbose_name='\u041f\u0441\u0435\u0432\u0434\u043e\u043d\u0438\u043c')),
                ('email', models.EmailField(max_length=255, null=True, verbose_name='\u0415\u043c\u0430\u0439\u043b', blank=True)),
                ('img_url', models.URLField(null=True)),
                ('gender', models.CharField(max_length=10, null=True, verbose_name='\u041f\u043e\u043b', blank=True)),
                ('phone', models.CharField(max_length=255, unique=True, null=True, verbose_name='\u0422\u0435\u043b\u0435\u0444\u043e\u043d', blank=True)),
                ('address', models.CharField(max_length=255, null=True, verbose_name='\u0410\u0434\u0440\u0435\u0441', blank=True)),
                ('bike', models.CharField(max_length=255, null=True, verbose_name='\u0411\u0430\u0439\u043a', blank=True)),
                ('backend', models.CharField(max_length=16, null=True, choices=[('vk', '\u0412\u041a\u043e\u043d\u0442\u0430\u043a\u0442\u0435'), ('twitter', 'Twitter'), ('facebook', 'Facebook')])),
                ('id_from_backend', models.CharField(max_length=32, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='\u0410\u043a\u0442\u0438\u0432\u0435\u043d?')),
                ('is_admin', models.BooleanField(default=False, verbose_name='\u0410\u0434\u043c\u0438\u043d\u0438\u0441\u0442\u0440\u0430\u0442\u043e\u0440?')),
            ],
            options={
                'verbose_name': '\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c',
                'verbose_name_plural': '\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0438',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('name_ru', models.CharField(max_length=128, null=True)),
                ('name_be', models.CharField(max_length=128, null=True)),
                ('name_en', models.CharField(max_length=128, null=True)),
                ('description', models.TextField()),
                ('description_ru', models.TextField(null=True)),
                ('description_be', models.TextField(null=True)),
                ('description_en', models.TextField(null=True)),
                ('image', models.ImageField(upload_to='thubnails/')),
            ],
            options={
            },
            bases=(models.Model,),
        ),

    ]
