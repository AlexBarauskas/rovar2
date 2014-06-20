from django.conf.urls.defaults import patterns, include, url

from views import *

urlpatterns = patterns(
    'api.views',
    url(r'^clients$', initialize_app, name="api_initialize_app"),

    url(r'^location$', location, name="api_location"),
    
    url(r'^points$', points, name="api_get_points"),
    url(r'^point/add$', add_point, name="api_add_point"),
    url(r'^point/offer$', point_offer, name="api_point_offer"),

    url(r'^tracks$', tracks, name="api_get_tracks"),

    url(r'^messages$', messages, name="api_messages"),
    url(r'^messages/read$', message_read, name="api_message_read"),

    )
