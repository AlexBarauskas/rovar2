# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns(
    'blog.views',
    url(r'^$', "blog", name="blog"),
    url(r'^(?P<post_id>\d+)/$', "post", name="blog_post"),
)
