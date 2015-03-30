from django.conf.urls.defaults import patterns, include, url


urlpatterns = patterns(
    'developers.views',
    url(r'widget/examples$', 'widget', name='widget_examle'),
    url(r'widget/onbike.js$', 'widget_js', name='widget_js'),
)
