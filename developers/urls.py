from django.conf.urls import patterns, include, url


urlpatterns = patterns(
    'developers.views',
    url(r'widget/$', 'index', name='dev_index'),
    url(r'widget/examples$', 'widget', name='widget_examle'),
    url(r'widget/settings/$', 'settings', name='widget_settings'),
    url(r'widget/onbike.js$', 'widget_js', name='widget_js'),
    
    url(r'utils/get-point$', 'url_to_id'),
)
