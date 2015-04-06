# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponse

import json
import base64
import re

from map.models import Location, Point

def index(request):
    return render_to_response('developers/index.html',
                              {'menu_item': ('index',),
                               },
                              context_instance=RequestContext(request))
    

def widget(request):
    data = {"location" : {"name": "Минск",
                          "bounds": [[53.73909273331522,27.24485246663044],[54.06090726668478,27.888481533369557]],
                          "center": [53.9, 27.566667],
                          "zoom": 12
                          },
            "points": [120, 417, 190, 154],
            "default_point": 417,
            "extra_info": True,
            "popup": True,
            "css": "",
            };
    root = "#widget-example"
    
    widget_type = request.GET.get('type', 'popup')
    if widget_type == 'map-embed':
        data["popup"] = False
        data["css"] = ".onbikewidget-point-info{display:none;}.onbikewidget-point-info.current{display: block;}#onbikewidget-info{left:40px;top:0;z-index: 10;position: absolute;background-color: rgba(255,255,255,0.7);width: 70%;padding:0.5em;max-width:20em;}"
    elif widget_type == 'embed':
        data["popup"] = False
        data["css"] = ".onbikewidget-point-info.current{background-color:#eee;}"
        root = "body"
    elif widget_type == 'embed-one':
        data["popup"] = False
        data["css"] = ".onbikewidget-point-info{display:none;}.onbikewidget-point-info.current{display: block;}"
        root = "body"
    data['root'] = root
    menu_item = ('examples', widget_type )
    return render_to_response('developers/widget-examples.html',
                              {'show_left_panel': True,
                               'data': _options_to_base64(data),
                               'type': widget_type,
                               'menu_item': menu_item
                               },
                              context_instance=RequestContext(request))


def settings(request):
    if request.method == "POST":
        print request.POST
    return render_to_response('developers/settings.html',
                              {'menu_item': ('settings',),
                               'locations': Location.objects.all()
                               },
                              context_instance=RequestContext(request))



def widget_js(request):
    options = base64.decodestring(request.GET.get('data', '')) or '{}'
    js = render_to_string('developers/js/dinamic-widget.js',
                          {'host': "onbike.by",
                           'options': options},
                          context_instance=RequestContext(request))
    return HttpResponse(js,
                        content_type = "text/javascript")


def url_to_id(request):
    path = request.GET.get('url', '').strip()
    point = re.findall('/(?P<slug>\w+)/(?P<uid>[\-_\w]+)$', path)
    if len(point) == 0:
        return HttpResponse(json.dumps({'point': None,
                                        'success': False,
                                        'message': u'Точка не найдена'}),
                            content_type = "text/json"
                            )
    ptype, uid = point[0]
    
    try:
        point = Point.objects.get(uid=uid,
                                  type__slug=ptype,
                                  location__name=request.GET.get('location'))
    except Exception, e:
        print e
        return HttpResponse(json.dumps({'point': None,
                                        'success': False,
                                        'message': u'Точка не найдена'}),
                            content_type = "text/json"
                            )
    return HttpResponse(json.dumps({'point': {'id': point.id, 'title': point.name},
                                    'success': True,
                                    'message': u'Точка "%s" добавлена в список' % point.name}),
                        content_type = "text/json"
                        )

def _options_to_base64(data={}):
    return base64.encodestring(json.dumps(data)).replace('\n','')
    
