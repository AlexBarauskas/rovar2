# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


ACCOUNT_BACKENDS = ((u'vk', u'ВКонтакте'),
                    (u'twitter', u'Twitter'),
                    (u'facebook', u'Facebook'),
                    )

class Account(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=128)
    img_url = models.URLField(null=True)
    backend = models.CharField(max_length=16, choices=ACCOUNT_BACKENDS, null=True)
    id_from_backend = models.CharField(max_length=32, null=True)
#ALTER TABLE "account_account" ALTER COLUMN "backend" DROP NOT NULL;
