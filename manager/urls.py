from django.conf.urls.defaults import patterns, include, url

from views import *

urlpatterns = patterns(
    'manager.urls',
    url(r'^$', index, name="manager_index"),
    
    url(r'^types/$', types, name="track_point_types"),
    url(r'^types/(?P<type_id>\d+)/del/$', type_delete, name="type-delete"),

    url(r'^tracks/$', default, name="manager_tracks"),
    url(r'^points/$', default, name="manager_points"),
    #url(r'tracks^$', default, name="manager_tracks"),
    
    )
