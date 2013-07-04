# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

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
    
    def obj_name(self):
        return "%s - %s" % (dict(OBJ_CHOICES)[self.obj], self.name)

    def __unicode__(self):
        return self.name

class PostManager(models.Manager):
    def get_links(self, acl):
        qs = self.get_query_set().extra(select={'acl_track': 'SELECT state FROM manager_track WHERE post_id=manager_post.id ',
                                                'acl_point': 'SELECT state FROM manager_point WHERE post_id=manager_post.id ',
                                                }).order_by('-created')
        links = {}
        for p in qs:
            if (p.acl_track or p.acl_track) and (p.acl_track or p.acl_track) <= acl:
                key = p.created.strftime('%d %B, %Y')
                l = links.get(key, [])
                l.append({'title': p.title,
                          'date': p.created,
                          'id': p.id})
                links[key] = l            
        return links


class Post(models.Model):
    title = models.CharField(u'Заголовок', max_length=128, null=False)
    text = models.TextField(u'Пост', default='')
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title

    objects = PostManager()


class Comment(models.Model):
    owner = models.ForeignKey(User)
    parent = models.ForeignKey('self', null=True)
    post = models.ForeignKey(Post)
    created = models.DateTimeField(auto_now_add=True)
    text = models.TextField(u'Комментарий', default='', blank=False)


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
    created = models.DateTimeField(auto_now_add=True)
    post = models.OneToOneField(Post, null=True)

    def __unicode__(self):
        return self.name


class EditorImage(models.Model):
    image = models.ImageField(upload_to="editor-images/")
    created = models.DateTimeField(auto_now_add=True)

