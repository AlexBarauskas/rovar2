# -*- coding: utf-8 -*-
from django.db import models
from account.models import User


class PostManager(models.Manager):
    def get_links(self, acl):
        qs = self.get_query_set().extra(select={'acl_track': 'SELECT state FROM map_track WHERE post_id=blog_post.id ',
                                                'acl_point': 'SELECT state FROM map_point WHERE post_id=blog_post.id ',
                                                }).order_by('-created')
        links = {}
        for p in qs:
            if (p.acl_track or p.acl_track) and (p.acl_track or p.acl_track) <= acl:
                key = p.created.strftime('%d %B, %Y')
                l = links.get(key, [])
                l.append({'title': p.title,
                          'date': p.created,
                          'id': p.id,
                          'P': p})
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
    owner = models.ForeignKey(User, verbose_name='comments')
    post = models.ForeignKey(Post)
    parent = models.ForeignKey('self', null=True)
    created = models.DateTimeField(auto_now_add=True)
    text = models.TextField(u'Комментарий', default='')

    def to_dict(self, lang=None):
        #translate = self.get_translation_obj(lang=lang)
        import calendar
        timestamp = calendar.timegm(self.created.timetuple())

        comment = {'id': self.pk,
                   'username': self.owner.username,
                   'is_auth': True, # Можно ли ответить? Пока да и всем
                   'message': self.text,
                   'timestamp': timestamp,
                   'status': 'success',
        }

        if self.parent:
            comment['parent_id'] = self.parent.pk
        else:
            comment['parent_id'] = None

        return comment

