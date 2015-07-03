# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        (b'contenttypes', b'__first__'),  # Add this line
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('img_url', models.URLField(null=True)),
                ('backend', models.CharField(max_length=16, null=True, choices=[('vk', '\u0412\u041a\u043e\u043d\u0442\u0430\u043a\u0442\u0435'), ('twitter', 'Twitter'), ('facebook', 'Facebook')])),
                ('id_from_backend', models.CharField(max_length=32, null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to=b'thubnails/')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
