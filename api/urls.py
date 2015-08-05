from django.conf.urls import patterns, include, url

from views import *

urlpatterns = patterns(
    'api.views',
    url(r'^clients$', initialize_app, name="api_initialize_app"),

    url(r'^locations$', locations, name="api_locations"),
    url(r'^location$', location, name="api_location"),

    url(r'^types$', get_types, name="api_types"),
    
    url(r'^points$', points, name="api_get_points"),
    url(r'^point/add$', add_point, name="api_add_point"),
    url(r'^point/offer$', point_offer, name="api_point_offer"),

    url(r'^tracks$', tracks, name="api_get_tracks"),

    url(r'^messages$', messages, name="api_messages"),
    url(r'^messages/read$', message_read, name="api_message_read"),

    url(r'^comments$', comments, name="api_get_comments"),
    url(r'^comment/add$', add_comment, name="api_add_comment"),

    url(r'^ratings$', ratings, name="api_get_ratings"),
    )
