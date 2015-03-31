# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponse

import json
import base64

@login_required
def widget(request):
    data = {"location" : {"name": "Минск",
                          "bounds": [[53.73909273331522,27.24485246663044],[54.06090726668478,27.888481533369557]],
                          "center": [53.9, 27.566667],
                          "zoom": 12
                          },
            "points": [120, 69, 190, 154],
            "default_point": 69,
            "extra_info": True,
            "popup": True,
            "css": "",
            };
    root = "#widget-example"
    
    widget_type = request.GET.get('type', 'popup')
    if widget_type == 'map-embed':
        data["popup"] = False
        data["css"] = ".onbikewidget-point-info{display:none;}.onbikewidget-point-info.current{display: block;}#onbikewidget-info{left:0;top:0;z-index: 10;position: absolute;background-color: rgba(255,255,255,0.7);width: 70%;margin-left:40px;padding:5px;max-width:300px;}#onbikewidget-map{position:absolute;width:100%;height:100%;top:0;left:0;}"
    elif widget_type == 'embed':
        data["popup"] = False
        data["css"] = ".onbikewidget-point-info{border:solid 1px #ddd;}.onbikewidget-point-info.current{background-color:#eee;}"
        root = "body"
    elif widget_type == 'embed-one':
        data["popup"] = False
        data["css"] = ".onbikewidget-point-info{display:none;}.onbikewidget-point-info.current{display: block;}"
        root = "body"
    data['root'] = root
    return render_to_response('developers/widget-examples.html',
                              {'show_left_panel': True,
                               'data': _options_to_base64(data),
                               'type': widget_type,                               
                               },
                              context_instance=RequestContext(request))

def widget_js(request):
    options = base64.decodestring(request.GET.get('data', '')) or '{}'
    js = render_to_string('developers/js/dinamic-widget.js',
                          {'host': "localhost:8000",
                           'options': options},
                          context_instance=RequestContext(request))
    return HttpResponse(js,
                        content_type = "text/javascript")


def _options_to_base64(data={}):
    return base64.encodestring(json.dumps(data)).replace('\n','')
    
