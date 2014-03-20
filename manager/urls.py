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
    url(r'^tracks/(?P<track_id>\d+)/edit-post/$', post_edit, name="post-edit-track"),

    url(r'^points/$', points, name="manager_points"),
    url(r'^points/(?P<type_id>\d+)/$', points, name="manager_points"),
    url(r'^points/add/$', point_edit, name="point-add"),
    url(r'^points/(?P<point_id>\d+)/edit/$', point_edit, name="point-edit"),
    url(r'^points/(?P<point_id>\d+)/delete/$', point_delete, name="point-delete"),
    url(r'^points/\d+/(?P<point_id>\d+)/delete/$', point_delete, name="point-delete"),
    url(r'^points/(?P<point_id>\d+)/edit-post/$', post_edit, name="post-edit-point"),

    url(r'^tiny/image_list.js$', js_image_list, name="tiny-image-list"),
    url(r'^(?P<img_id>\d+)/delete/$', editor_img_del, name="editor_img_del"),
    url(r'^points/(?P<point_id>\d+)/edit/(?P<img_id>\d+)/delete/$', photo_img_del, name="photo_img_del")
    )


