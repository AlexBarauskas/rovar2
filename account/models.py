# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


ACCOUNT_BACKENDS = (('vk', u'ВКонтакте'),
                    ('twitter', u'Твиттер'),
                    ('facebook', u'Facebook'),
                    )

class Account(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=128)
    img_url = models.URLField(null=True)
    backend = models.CharField(max_length=16, choices=ACCOUNT_BACKENDS)
    id_from_backend = models.CharField(max_length=32, choices=ACCOUNT_BACKENDS)
    #token = models.CharField(max_length=128)
