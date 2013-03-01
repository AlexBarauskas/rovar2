from django.conf.urls.defaults import patterns, include, url

from views import *

urlpatterns = patterns(
    'map.urls',
    #url(r'^$', index, name="manager_index"),

    url(r'^available-tracks/$', get_available_tracks, name="get_available_tracks"),
    
    url(r'^track/$', track, name="get_track"),
    url(r'^track/(?P<track_id>\d+)/$', track, name="get_track_by_id"),
    
    )
