# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url

from views import *

urlpatterns = patterns(
    'manager.urls',
    url(r'^$', index, name="manager_index"),
    
    url(r'^types/$', types, name="track_point_types"),
    url(r'^types/(?P<type_id>\d+)/delete/$', type_delete, name="type-delete"),

    url(r'^tracks/$', tracks, name="manager_tracks"),
    url(r'^tracks/add/$', track_edit, name="track-add"),
    url(r'^tracks/(?P<track_id>\d+)/edit/$', track_edit, name="track-edit"),
    url(r'^tracks/(?P<track_id>\d+)/delete/$', track_delete, name="track-delete"),

    url(r'^points/$', default, name="manager_points"),
    #url(r'tracks^$', default, name="manager_tracks"),
    
    )
