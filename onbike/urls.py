# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.views.generic.base import RedirectView
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse

from map.sitemap import LocationSitemap, Location

class StaticSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return ['info', 'dev_index', 'widget_examle']

    def location(self, item):
        return reverse(item)

SITEMAPS = {
    'static' : StaticSitemap(),
    }
for l in Location.objects.all():
    SITEMAPS[l.name] = LocationSitemap(location=l)


urlpatterns = patterns(
    '',
    #url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': {'/': StaticViewSitemap()}}),
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.index', {'sitemaps': SITEMAPS}),
    url(r'^sitemap-(?P<section>.+)\.xml$', 'django.contrib.sitemaps.views.sitemap', 
        {'sitemaps': SITEMAPS,
         #'template_name': 'qartez/rel_alternate_hreflang_sitemap.xml'
         }),

    url(r'^robots.txt$', 'onbike.views.robots', name='home'),
    url(r'^qr.png$', 'onbike.views.make_qr', name='make_qr'),
    url(r'^qr/$', 'onbike.views.qr_redirect', name='qr_redirect'),

    url(r'^$', 'onbike.views.home', name='home'),
    url(r'^short-home/$', 'onbike.views.short_home', name='short_home'),
    
    
    url(r'^info/$', TemplateView.as_view(template_name="info.html"), name='info'),
    url(r'^language/$', 'onbike.views.set_language', name='set_language'),
    #url(r'^location/$', 'onbike.views.set_location', name='set_location'),
    url(r'^manager/', include('manager.urls')),
    url(r'^map/', include('map.urls')),
    url(r'^blog/', include('blog.urls')),
    url(r'^api/doc.html$', 'onbike.views.api_doc', name="api_doc"),
    url(r'^api/', include('api.urls')),
    url(r'^dev/', include('developers.urls')),

    url(r'^account/logout/$', 'django.contrib.auth.views.logout',
        { 'next_page' : '/' }, name="logout"),
    #url(r'^account/login/$', 'django.contrib.auth.views.login',
    #    {'template_name': 'login.html'},
    #    name="account_login"),
    # url(r'^account/login/$', RedirectView.as_view(url='/', permanent=False)),

    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^logout/$', 'account.views.logout'),
    # Нам нужно твоё мыло:) если некоторое из провайдеров не вернули его
    url(r'^email/$', 'account.views.require_email', name='require_email'),

    url(r'^account/', include('account.urls')),

#    url(r'^login/$','django.contrib.auth.views.login',{ 'template_name' : 'login.html'},name="login"),

    # url(r'^rovar2/', include('rovar2.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^i18n/', include('django.conf.urls.i18n')),

    url(r'^admin/', include(admin.site.urls)),


    #url(r'^(?P<slug>\w+)/(?P<uid>[\-_\w]+)$', 'onbike.views.home', name='home_uid'),
    #url(r'^(?P<uid>\d+\-\w)/$', 'onbike.views.home', name='home_uid'),


)

if settings.DEBUG:
    urlpatterns += patterns('',
                            url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
                                { 'document_root' : settings.MEDIA_ROOT }),
                            url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
                                { 'document_root' : settings.STATIC_ROOT }),
                            )


urlpatterns += patterns(
    '',
    url(r'^(?P<location_name>\w+)/$', 'onbike.views.show_location', name='show_location'),
    url(r'^(?P<location_name>\w+)/(?P<slug>[\w\-]+)/$', 'onbike.views.show_category', name='show_category'),
    url(r'^(?P<location_name>\w+)/(?P<slug>[\w\-]+)/(?P<uid>[\-\+\.\%_\w]+)$', 'onbike.views.show_object', name='show_object'),
    )
