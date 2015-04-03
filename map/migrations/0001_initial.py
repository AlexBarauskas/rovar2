# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=16)),
                ('display_name', models.CharField(max_length=24, null=True)),
                ('center_lat', models.FloatField()),
                ('center_lng', models.FloatField()),
                ('radius', models.FloatField()),
                ('default', models.BooleanField(default=False)),
                ('admins', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField(default=b'', null=True, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=b'photos/')),
                ('description', models.TextField(default=b'', null=True, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435')),
                ('offer', models.ForeignKey(to='map.Offer', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Point',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435')),
                ('state', models.CharField(default=b'2', max_length=1, verbose_name='\u0414\u043e\u0441\u0442\u0443\u043f', choices=[(b'0', '\u0412\u0441\u0435 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0438'), (b'1', '\u0410\u0432\u0442\u043e\u0440\u0438\u0437\u043e\u0432\u0430\u043d\u043d\u044b\u0435 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0438'), (b'2', '\u0422\u043e\u043b\u044c\u043a\u043e \u0430\u0434\u043c\u0438\u043d\u0438\u0441\u0442\u0440\u0430\u0442\u043e\u0440'), (b'3', '\u041d\u0438\u043a\u0442\u043e')])),
                ('description', models.CharField(default=b'', max_length=256, verbose_name='\u041a\u0440\u0430\u0442\u043a\u043e\u0435 \u043e\u043f\u0438\u0441\u0430\u043d\u0438\u0435', blank=True)),
                ('coordinates', models.TextField(default=b'[]', verbose_name='\u041a\u043e\u043e\u0440\u0434\u0438\u043d\u0430\u0442\u044b')),
                ('address', models.CharField(max_length=256, verbose_name='\u0410\u0434\u0440\u0435\u0441')),
                ('phones', models.CharField(max_length=128, null=True, verbose_name='\u0422\u0435\u043b\u0435\u0444\u043e\u043d\u044b', blank=True)),
                ('website', models.URLField(null=True, verbose_name='\u0421\u0430\u0439\u0442', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now_add=True)),
                ('uid', models.CharField(max_length=24, null=True, blank=True)),
                ('location', models.ForeignKey(to='map.Location', null=True)),
                ('post', models.OneToOneField(null=True, to='blog.Post')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435')),
                ('state', models.CharField(default=b'2', max_length=1, verbose_name='\u0414\u043e\u0441\u0442\u0443\u043f', choices=[(b'0', '\u0412\u0441\u0435 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0438'), (b'1', '\u0410\u0432\u0442\u043e\u0440\u0438\u0437\u043e\u0432\u0430\u043d\u043d\u044b\u0435 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0438'), (b'2', '\u0422\u043e\u043b\u044c\u043a\u043e \u0430\u0434\u043c\u0438\u043d\u0438\u0441\u0442\u0440\u0430\u0442\u043e\u0440'), (b'3', '\u041d\u0438\u043a\u0442\u043e')])),
                ('description', models.CharField(max_length=256, verbose_name='\u041a\u0440\u0430\u0442\u043a\u043e\u0435 \u043e\u043f\u0438\u0441\u0430\u043d\u0438\u0435')),
                ('coordinates', models.TextField(default=b'[]', verbose_name='\u041a\u043e\u043e\u0440\u0434\u0438\u043d\u0430\u0442\u044b')),
                ('video', models.TextField(default=b'', verbose_name='\u0421\u0441\u044b\u043b\u043a\u0430 \u043d\u0430 \u0432\u0438\u0434\u0435\u043e', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('duration', models.PositiveIntegerField(null=True, verbose_name='\u0414\u043b\u0438\u0442\u0435\u043b\u044c\u043d\u043e\u0441\u0442\u044c', blank=True)),
                ('uid', models.CharField(max_length=16, null=True)),
                ('color', models.CharField(default=b'#0000FF', max_length=7, verbose_name='\u0426\u0432\u0435\u0442')),
                ('location', models.ForeignKey(to='map.Location', null=True)),
                ('post', models.OneToOneField(null=True, to='blog.Post')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Translation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language', models.CharField(max_length=2)),
                ('name', models.CharField(max_length=128, verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435', blank=True)),
                ('description', models.CharField(max_length=256, verbose_name='\u041a\u0440\u0430\u0442\u043a\u043e\u0435 \u043e\u043f\u0438\u0441\u0430\u043d\u0438\u0435', blank=True)),
                ('address', models.CharField(max_length=256, null=True, verbose_name='\u0410\u0434\u0440\u0435\u0441', blank=True)),
                ('point', models.ForeignKey(to='map.Point', null=True)),
                ('track', models.ForeignKey(to='map.Track', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('obj', models.CharField(default=b't', max_length=1, verbose_name='\u041e\u0431\u044a\u0435\u043a\u0442', choices=[(b't', '\u041c\u0430\u0440\u0448\u0440\u0443\u0442'), (b'p', '\u0422\u043e\u0447\u043a\u0430'), (b'o', '\u0414\u0440\u0443\u0433\u043e\u0435')])),
                ('active', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=64, verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435')),
                ('color', models.CharField(default=b'#0000FF', max_length=7, verbose_name='\u0426\u0432\u0435\u0442')),
                ('image', models.ImageField(upload_to=b'icons/', null=True, verbose_name='Small pin', blank=True)),
                ('image2', models.ImageField(upload_to=b'icons/', null=True, verbose_name='Pin', blank=True)),
                ('slug', models.CharField(default=b'other', max_length=24, verbose_name='Text ID')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='track',
            name='type',
            field=models.ForeignKey(to='map.Type'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='point',
            name='type',
            field=models.ForeignKey(to='map.Type'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='photo',
            name='point',
            field=models.ForeignKey(to='map.Point', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='photo',
            name='track',
            field=models.ForeignKey(to='map.Track', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='offer',
            name='point',
            field=models.ForeignKey(to='map.Point', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='offer',
            name='track',
            field=models.ForeignKey(to='map.Track', null=True),
            preserve_default=True,
        ),
    ]
