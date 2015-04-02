from django.conf.urls import patterns, include, url

from views import *

urlpatterns = patterns(
    'map.views',
    #url(r'^$', index, name="manager_index"),

    url(r'^available-tracks/$', get_available_tracks, name="get_available_tracks"),
    url(r'^available-points/$', get_available_points, name="get_available_points"),
    
    url(r'^track/$', track, name="get_track"),
    url(r'^track/(?P<track_id>\d+)/$', track, name="get_track_by_id"),

    url(r'^point/$', point, name="get_point"),
    url(r'^point/(?P<point_id>\d+)/$', point, name="get_point_by_id"),
    url(r'^all-points/$', all_points, name="all_points"),

    url(r'^tile/(?P<z>\d+)/(?P<x>\d+)/(?P<y>\d+).png$', tile, name="map_tile"),


    )
