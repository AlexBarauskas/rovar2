from django.conf.urls.defaults import patterns, include, url

from views import *

urlpatterns = patterns(
    'map.urls',
    #url(r'^$', index, name="manager_index"),
    
    url(r'^track/$', track, name="get_track"),
    
    )
