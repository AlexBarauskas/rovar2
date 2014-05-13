# -*- coding: utf-8 -*-
from django.db import models
import time
import random
import hashlib

from map.models import Track, Point, Type, Photo, Offer


def make_uid():
    return hashlib.md5('%s-%s' % (time.time(), random.random())).hexdigest()


class Application(models.Model):
    uid = models.CharField(max_length=56, default=make_uid, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def add_message(self, point=None, track=None, method='a', email=None, description=None):
        Message.objects.create(point=point, track=track, app=self, method=method,
                               email=email, description=description)
        

    
STATE_CHOICES = (('m', u'На рассмотрении модератором'),
                 ('f', u'Для отправки'),
                 ('s', u'Отправлено'),
                 ('r', u'Прочитано'),
                 )


    
class Message(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    app = models.ForeignKey(Application)
    point = models.ForeignKey(Point, null=True)
    track = models.ForeignKey(Track, null=True)
    state = models.CharField(max_length=1,
                             choices=STATE_CHOICES,
                             default='m')
    method = models.CharField(max_length=1,
                             choices=(('a', u'Добавление точки'),
                                      ('u', u'Предложение на изменение'),
                                      ),
                             default='a')
    message = models.TextField(default=u'Ваше предложение принято.')
    email = models.EmailField(null=True)
    description = models.TextField(u'Описание', default='', null=True)
