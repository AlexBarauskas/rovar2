# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20150809_1410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='owner',
            field=models.ForeignKey(related_name='comments', verbose_name=b'comments', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
