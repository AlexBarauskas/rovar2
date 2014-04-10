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

    def add_message(self, point=None, track=None):
        Message.objects.create(point=point, track=track, app=self)
        

    
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
    message = models.TextField(default=u'Ваше предложение принято.')
