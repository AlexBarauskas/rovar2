from django.conf.urls.defaults import patterns, include, url
from django.conf import settings


urlpatterns = patterns(
    'account.views',
    url(r'^$', 'login_page', name='account_login'),
    url(r'^return/(?P<backend_name>\w+)/$', 'login_return', name='account_return'),
)
