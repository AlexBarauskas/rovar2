# -*- coding: utf-8 -*-
from django.db import models

OBJ_CHOICES = (('t', u'Маршрут'),
               ('p', u'Точка'),
               ('o', u'Другое'),
               )

class Type(models.Model):
    obj = models.CharField(u'Объект',
                           max_length=1,
                           choices=OBJ_CHOICES,
                           default='t')
    active = models.BooleanField(default=False, blank=False)
    name = models.CharField(u'Наименование', max_length=256, null=False)
    
    def obj_name(self):
        return dict(OBJ_CHOICES)[self.obj]

    def __unicode__(self):
        return "%s - %s" % (self.obj_name(), self.name)
