from django.conf.urls.defaults import patterns, include, url

from views import *

urlpatterns = patterns(
    'api.views',
    url(r'^clients$', initialize_app, name="api_initialize_app"),
    url(r'^points$', points, name="api_get_points"),
    url(r'^point/add$', add_point, name="api_add_point"),

    url(r'^messages$', messages, name="api_messages"),
    url(r'^messages/read$', message_read, name="api_message_read"),

    )
