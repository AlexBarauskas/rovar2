# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.conf import settings

from blog.models import Post
import json

OBJ_CHOICES = (('t', u'Маршрут'),
               ('p', u'Точка'),
               ('o', u'Другое'),
               )

ACCESS = (('0', u'Все пользователи'),
          ('1', u'Авторизованные пользователи'),
          ('2', u'Только администратор'),
          ('3', u'Никто'),
          )

TYPEIDS = {"entertainment": 7,
           "bikerental": 6,
           "shop": 5,
           "service": 2,
           "parking": 3,
           }
IDSTYPE =  {2: 'service', 3: 'parking', 5: 'shop', 6: 'bikerental', 7: 'entertainment'}


class Type(models.Model):
    obj = models.CharField(u'Объект',
                           max_length=1,
                           choices=OBJ_CHOICES,
                           default='t')
    active = models.BooleanField(default=False, blank=False)
    name = models.CharField(u'Наименование', max_length=64, null=False)
    color = models.CharField(u'Цвет', max_length=7, default="#0000FF")
    image = models.ImageField(u'Small pin', upload_to="icons/", null=True, blank=True)
    image2 = models.ImageField(u'Pin', upload_to="icons/", null=True, blank=True)
    slug = models.CharField(u'Text ID', max_length=24, default="other")
    # ALTER TABLE map_type ADD  "slug" varchar(24) NOT NULL default 'other';

    
    def count_items(self):
        try:
            return self.track_set.filter(state__lte=self.acl).count() or self.point_set.filter(state__lte=self.acl).count()
        except:
            return self.track_set.count() or self.point_set.count()
        
    
    def obj_name(self):
        return "%s - %s" % (dict(OBJ_CHOICES)[self.obj], self.name)

    def get_slug(self):
        return IDSTYPE.get(self.id, 'other')

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

    def to_dict(self):
        track = {'route': json.loads(self.coordinates),
                 'title': self.name,
                 'description': self.description,
                 'video': self.video or '',
                 'id': self.id,
                 'type': [self.type.obj, '%s' % self.type.id],
                 'color': self.color or self.type.color,
                 'uid': self.uid,
                 'type_name': self.type.name,
                 'type_slug': self.type.slug,
                 }
        if self.duration:
            track['duration'] = '%s мин' % self.duration
        if self.post:
            track['post_url'] = reverse('blog_post', args=[self.post.id])
        if self.type.image:
            track['marker_a'] = self.type.image.url
            track['marker_b'] = self.type.image.url
        if self.type.image2:
            track['marker_b'] = self.type.image2.url
        return track


    def __unicode__(self):
        return self.name


def iso_phone(number):
    res = tuple([i for i in number if i>='0' and i<='9'])
    if len(res) == 12:
        return "+%s%s%s (%s%s) %s%s%s-%s%s-%s%s" % res
    elif len(res) == 9:
        return "+375 (%s%s) %s%s%s-%s%s-%s%s" % res
    elif len(res) == 7:
        return "+375 (29) %s%s%s-%s%s-%s%s" % res
    res = ''.join(res)
    if res.startswith('80') and len(res) == 11:
        return "+375 (%s%s) %s%s%s-%s%s-%s%s" % tuple(res[2:])
    if len(res)>0 and len(res)%12 == 0 :
        return ', '.join([iso_phone(res[n*12:(n+1)*12]) for n in range(len(res)/12)])
    return res
        
    
class PointManager(models.Manager):
    def to_translate_manager(self):
        return render_to_string('manager/translate_point.txt',
                         {'points': self.all()}
                         )
    def from_translate_manager(self, input_string):
        _points = [i.split("##") for i in input_string.split("###->") if i.strip()]
        points = {}
        for p in _points:
            pid = p[0].strip()
            points[pid] = {}
            
            for lang in p[1:]:
                lang_code = lang[:2]
                points[pid][lang_code] = {}
                fields = lang[2:]
                for f in fields.split('#'):
                    f = f.strip()
                    n = f.find('\n')
                    if n > 0:
                        f_name = f[:n].strip()
                        f_value = f[n:].strip()
                    else:
                        f_name = f.strip()
                        f_value = ""
                    if f_name:
                        points[pid][lang_code][f_name] = f_value
        for pid, trans in points.iteritems():
            try:
                p = Point.objects.get(id=pid)
            except Point.DoesNotExist:
                p = None
            if p is not None:
                for lang, fields in trans.iteritems():
                    t, c = Translation.objects.get_or_create(point=p, language=lang)
                    Translation.objects.filter(id=t.id).update(**fields)
        
                    

## Phone template +375 (29) 662-73-44
## phone_re=re.compile('(\+\d\d\d \(\d\d\) \d\d\d\-\d\d\-\d\d)')
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

    phones = models.CharField(u'Телефоны', max_length=128, blank=True, null=True)
    website = models.URLField(u'Сайт', blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    post = models.OneToOneField(Post, null=True)
    uid = models.CharField(max_length=24, null=True)

    objects = PointManager()

    def save(self, *args, **kwargs):
        if self.phones:
            self.phones = ', '.join([j for j in [iso_phone(j) for j in self.phones.split(',')] if j])
        res = super(Point, self).save(*args, **kwargs)
        if not self.uid:
            self.uid = "%s-%s" % (self.id, self.type.obj)
            self.save()
        return res

    def __unicode__(self):
        return self.name


    def initTransList(self):
        res = []
        for lan_code, lan_name in settings.LANGUAGES:
            to = self.get_translation_obj(lang=lan_code)
            res.append({'language': lan_code,
                        'name': to.name,
                        'address': to.address or '',
                        'description': to.description
                        })
        return res

    def get_translation_obj(self, lang=None):
        if lang is None or lang == settings.LANGUAGE_CODE:
            return self
        tr = Translation.objects.get_or_create(point=self, language=lang)
        return tr[0]

    def to_dict(self, lang=None):
        translate = self.get_translation_obj(lang=lang)
        
        point = {'coordinates': json.loads(self.coordinates),
                 'title': translate.name or self.name,
                 'description': translate.description or self.description,
                 'id': self.id,
                 'color': self.type.color,
                 'marker': '/static/images/Parking.png',
                 'marker_active': '/static/images/Parking.png',
                 'status': 'success',
                 'images': [ph.image.url for ph in  self.photo_set.all()],
                 'address': translate.address or self.address,
                 'uid': self.uid,
                 'type_slug': self.type.slug,
                 'type_name': self.type.name,
                 'website': self.website
                 }
        if self.phones:
            point['phones'] = self.phones
        else:
            point['phones'] = ''
        if self.type.image:
            point['marker'] = self.type.image.url
            point['marker_active'] = self.type.image.url
        if self.type.image2:
            point['marker_active'] = self.type.image2.url
        point['type'] = [self.type.obj, '%s' % self.type.id]
        return point


class Photo(models.Model):
    point = models.ForeignKey(Point, null=True)
    track = models.ForeignKey(Track, null=True)
    image = models.ImageField(upload_to="photos/")
    description = models.TextField(u'Описание', default='', null=True)


class Offer(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    point = models.ForeignKey(Point, null=True)
    track = models.ForeignKey(Track, null=True)
    description = models.TextField(u'Описание', default='', null=True)
    

class Translation(models.Model):
    point = models.ForeignKey(Point, null=True)
    track = models.ForeignKey(Track, null=True)
    language = models.CharField(max_length=2, null=False)
    
    name = models.CharField(u'Наименование', max_length=128, null=False, blank=True)
    description = models.CharField(u'Краткое описание', max_length=256, null=False, blank=True)
    address = models.CharField(u'Адрес', max_length=256, null=True, blank=True)
