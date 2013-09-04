# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from blog.models import Post

OBJ_CHOICES = (('t', u'Маршрут'),
               ('p', u'Точка'),
               ('o', u'Другое'),
               )

ACCESS = (('0', u'Все пользователи'),
          ('1', u'Авторизованные пользователи'),
          ('2', u'Только администратор'),
          ('3', u'Никто'),
          )


class Type(models.Model):
    obj = models.CharField(u'Объект',
                           max_length=1,
                           choices=OBJ_CHOICES,
                           default='t')
    active = models.BooleanField(default=False, blank=False)
    name = models.CharField(u'Наименование', max_length=64, null=False)
    color = models.CharField(u'Цвет', max_length=7, default="#0000FF")
    image = models.ImageField(upload_to="icons/", null=True, blank=True)
    
    def count_items(self):
        return self.track_set.count() or self.point_set.count()
    
    def obj_name(self):
        return "%s - %s" % (dict(OBJ_CHOICES)[self.obj], self.name)

    def __unicode__(self):
        return self.name


class Track(models.Model):
    name = models.CharField(u'Наименование', max_length=128, null=False)
    state = models.CharField(u'Доступ',
                           max_length=1,
                           choices=ACCESS,
                           default='2')
    type = models.ForeignKey(Type,
                             limit_choices_to={'obj': 't'})
    description = models.CharField(u'Краткое описание', max_length=256, null=False)
    coordinates = models.TextField(u'Координаты', default='[]')
    video = models.TextField(u'Ссылка на видео', default='', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    post = models.OneToOneField(Post, null=True)
    duration = models.PositiveIntegerField(u'Длительность',null=True, blank=True)
    uid = models.CharField(max_length=16, null=True)
    color = models.CharField(u'Цвет', max_length=7, default="#0000FF")

    def save(self, *args, **kwargs):
        res = super(Track, self).save(*args, **kwargs)
        if not self.uid:
            self.uid = "%s-%s" % (self.id, self.type.obj)
            self.save()
        return res

    def __unicode__(self):
        return self.name


class Point(models.Model):
    name = models.CharField(u'Наименование', max_length=128, null=False)
    state = models.CharField(u'Доступ',
                           max_length=1,
                           choices=ACCESS,
                           default='2')
    type = models.ForeignKey(Type,
                             limit_choices_to={'obj': 'p'})
    description = models.CharField(u'Краткое описание', max_length=256, null=False)
    coordinates = models.TextField(u'Координаты', default='[]')
    address = models.CharField(u'Адрес', max_length=256, null=False)
    created = models.DateTimeField(auto_now_add=True)
    post = models.OneToOneField(Post, null=True)
    uid = models.CharField(max_length=24, null=True)

    def save(self, *args, **kwargs):
        res = super(Point, self).save(*args, **kwargs)
        if not self.uid:
            self.uid = "%s-%s" % (self.id, self.type.obj)
            self.save()
        return res

    def __unicode__(self):
        return self.name


class Photo(models.Model):
    point = models.ForeignKey(Point, null=True)
    track = models.ForeignKey(Track, null=True)
    image = models.ImageField(upload_to="photos/")
    description = models.TextField(u'Описание', default='', null=True)
