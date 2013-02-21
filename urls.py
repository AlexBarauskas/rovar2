from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'rovar2.views.home', name='home'),

    url(r'^manager/', include('manager.urls')),

    url(r'^login/$','django.contrib.auth.views.login',{ 'template_name' : 'login.html'},name="login"),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        { 'next_page' : '/' }, name="logout"),

    # url(r'^rovar2/', include('rovar2.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
