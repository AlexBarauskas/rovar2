from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'onbike.views.home', name='home'),
    
    url(r'^info/$', 'onbike.views.info', name='info'),
    url(r'^manager/', include('manager.urls')),
    url(r'^map/', include('map.urls')),
    url(r'^blog/', include('blog.urls')),

    url(r'^account/logout/$', 'django.contrib.auth.views.logout',
        { 'next_page' : '/' }, name="logout"),
    url(r'^account/', include('account.urls')),
                       
#    url(r'^login/$','django.contrib.auth.views.login',{ 'template_name' : 'login.html'},name="login"),

    # url(r'^rovar2/', include('rovar2.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),


    url(r'^(?P<uid>\d+\-\w)/$', 'onbike.views.home', name='home_uid'),

)

if settings.DEBUG:
    urlpatterns += patterns('',
                            url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
                                { 'document_root' : settings.MEDIA_ROOT }),
                            #url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
                            #    { 'document_root' : settings.STATIC_ROOT }),

                            )
