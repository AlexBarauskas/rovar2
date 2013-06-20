# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from manager.models import *
from django.template import RequestContext

def home(request):
    acl = '0'
    if request.user.is_authenticated():
        acl = '1'
        if request.user.is_staff:
            acl = '2'

    try:
        parking_type = Type.objects.get(obj='p', name=u"Велопарковки")
        parkings = parking_type.point_set.filter(state__lte=acl).count()
    except:
        parkings = 0

    try:
        services_type = Type.objects.get(obj='p', name=u"Сервисы")
        services = services_type.point_set.filter(state__lte=acl).count()
    except:
        services = 0

    return render_to_response('home.html',
                              {'tracks': Track.objects.filter(state__lte=acl),
                               'services': services,
                               'parkings': parkings
                               },
                              context_instance=RequestContext(request))
